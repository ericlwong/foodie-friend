"""Server for Foodie Friend app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
from jinja2 import StrictUndefined
from passlib.hash import argon2
import utils
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.app_context().push()

@app.route("/")
def show_homepage():
    """View homepage."""

    return render_template("homepage.html", user=utils.is_logged_in())

@app.route("/login")
def show_login():
    """View login page."""

    return render_template("login.html")

@app.route("/login", methods=["POST"])
def handle_login():
    """Log user into account."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user and user.email == email and argon2.verify(password, user.password):
        session["user"] = user.user_id
        flash("Login successful!", "success")

        return redirect("/")
    else:
        flash("Incorrect email and password. Please try again.", "danger")

        return redirect("/login")
    
@app.route("/signup")
def show_signup():
    """View sign up page."""

    return render_template("signup.html", states=utils.STATES)

@app.route("/signup", methods=["POST"])
def create_account():
    """Create a new user account."""

    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    address = request.form.get("address")
    address_2 = request.form.get("address-2")
    city = request.form.get("city")
    state = request.form.get("state")
    zipcode = request.form.get("zipcode")

    if (not email or not password or not fname or not lname or 
            not address or not city or not state or not zipcode):
        flash("Please enter all required fields.", "danger")
        
        return redirect("/signup")

    user = crud.get_user_by_email(email)

    if user:
        flash("Email already in use. Please use another one or log in with existing email.", "danger")

        return redirect("/signup")
    else:
        hashed_password = argon2.hash(password)
        new_user = crud.create_user(fname, lname, email, hashed_password, city, 
                                state, zipcode, address, address_2)
        
        db.session.add(new_user)
        db.session.commit()

        session["user"] = new_user.user_id
        flash("Account created and logged in!", "success")

        return redirect("/")
    
@app.route("/logout")
def handle_logout():
    """Log user out of account."""

    if "user" in session:
        del session["user"]
        flash("Logged out successfully!", "success") 
    else:
        flash("You are not currently logged in.", "info")

    return redirect("/")

# @app.route("/users")
# def show_users():
#     """View users."""

#     users = crud.get_users()

#     return render_template("all_users.html", users=users, user=utils.is_logged_in())

@app.route("/users/<user_id>")
def show_user_profile(user_id):
    """View a particular user's profile."""

    user = crud.get_user_by_id(user_id)

    # Can only access the logged-in user's profile
    if "user" in session and user.user_id == session["user"]:
        return render_template("profile.html", user=user, states=utils.STATES)
    else:
        return redirect("/")

@app.route("/users/<user_id>/create-list", methods=["POST"])
def create_new_favorites_list(user_id):
    """Create a new Favorites List for a particular user."""

    list_name = request.form.get("list-name")
    user = crud.get_user_by_id(user_id)
    favorites_list = crud.create_user_favorites_list(user, list_name)

    db.session.add(favorites_list)
    db.session.commit()

    flash("A new list has been created successfully!", "success")

    return redirect(f"/users/{user_id}")

@app.route("/restaurants")
def show_restaurants():
    """View restaurants."""

    restaurants = crud.get_restaurants()

    return render_template("all_restaurants.html", restaurants=restaurants, user=utils.is_logged_in())

@app.route("/restaurants/<restaurant_id>")
def show_restaurant(restaurant_id):
    """View a particular restaurant."""

    restaurant = crud.get_restaurant_by_id(restaurant_id)

    if restaurant.phone_number:
        restaurant_phone = utils.format_phone_number(restaurant.phone_number)
    else:
        restaurant_phone = None
        
    yelp_reviews = restaurant.yelp_reviews
    user_reviews = restaurant.user_reviews
    images = restaurant.images

    return render_template("restaurant_details.html", restaurant=restaurant, restaurant_phone_number=restaurant_phone,
                           yelp_reviews=yelp_reviews, user_reviews=user_reviews, images=images, user=utils.is_logged_in())

@app.route("/search")
def search_restaurants():
    """Search for restaurants."""

    query = request.args.get("query")
    location = request.args.get("location")
    try:
        city, state = location.split(",")
        city = city.strip()
        state= state.strip()
    except:
        flash("Please input both a city and state. Ex: San Francisco, CA", "danger")
        return redirect("/")

    call_yelp = False
    new_query = None
    restaurants = crud.get_restaurants_by_term_location(query, city, state)
    # If matched restaurants in DB is less than 10, requery DB by category
    if len(restaurants) < 10 and len(restaurants) > 0:
        for category in restaurants[0].categories:
            if category != "restaurants":
                new_query = category
                for result in crud.get_restaurants_by_term_location(category, city, state):
                    if result not in restaurants:
                        restaurants.append(result)
                break
        # If matched restaurants is still less than 10, call Yelp's API for more
        if len(restaurants) < 10:
            call_yelp = True
    else:
        new_query = query # Set Yelp query to be original search term
        call_yelp = True

    if call_yelp:
        restaurants.extend(utils.search_yelp_restaurants(new_query, location))

    return render_template("searched_restaurants.html", query=query, restaurants=restaurants, 
                           location=location, user=utils.is_logged_in())

@app.route("/write-review")
def show_review_form():
    """View Review Form page."""

    restaurant_id = request.args.get("restaurant")
    restaurant = crud.get_restaurant_by_id(restaurant_id)

    return render_template("write_review.html", restaurant=restaurant, user=utils.is_logged_in())

@app.route("/write-review", methods=["POST"])
def create_review():
    """Create a User Review for a particular restaurant."""

    if "user" in session:
        restaurant_id = request.form.get("restaurant")
        rating = request.form.get("rating")
        review = request.form.get("review")
        print(f"Restaurant ID: {restaurant_id}")
        print(f"Rating: {rating}")
        print(f"Review: {review}")

        try:
            user = crud.get_user_by_id(session["user"])
            restaurant = crud.get_restaurant_by_id(restaurant_id)
            review = crud.create_user_review(user, restaurant, review, rating)

            db.session.add(review)
            db.session.commit() 

            flash(f"You have successfully left a review for {restaurant.name}!", "success")
        except Exception as e:
            db.session.rollback()
            print(e)

        return redirect(f"/restaurants/{restaurant_id}")
    else:
        flash("Please log in before leaving a review.", "info")

        return redirect("/")

@app.route("/update/<user_id>/details", methods=["POST"])
def update_user_details(user_id):
    """Update account details of a particular user."""

    email = request.form.get("email")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    address = request.form.get("address")
    address_2 = request.form.get("address_2")
    city = request.form.get("city")
    state = request.form.get("state")
    zipcode = request.form.get("zipcode")

    if (not email or not fname or not lname or 
        not address or not city or not state or not zipcode):
        flash("Please enter all required fields.", "danger")
        
        return redirect(f"/users/{user_id}")

    user = crud.get_user_by_id(user_id)

    crud.set_user_email(user, email)
    crud.set_user_fname(user, fname)
    crud.set_user_lname(user, lname)
    crud.set_user_address(user, address)
    crud.set_user_address_2(user, address_2)
    crud.set_user_city(user, city)
    crud.set_user_state(user, state)
    crud.set_user_zipcode(user, zipcode)
    crud.set_update_at_time(user)

    db.session.commit()

    flash("Account details updated successfully!", "success")

    return redirect(f"/users/{user_id}")

@app.route("/update/<user_id>/password", methods=["POST"])
def update_user_password(user_id):
    """Update password of a particular user."""

    new_password = request.form.get("password")
    confirm_password = request.form.get("confirm-password")

    user = crud.get_user_by_id(user_id)

    if new_password and confirm_password:
        if new_password == confirm_password:
            hashed_new_password = argon2.hash(new_password)
            crud.set_user_password(user, hashed_new_password)
            db.session.commit()

            flash("Your password has been updated successfully!", "success")

            return redirect(f"/users/{user_id}")
        else:
            flash("Passwords do not match. Please try again.", "danger")
            return redirect(f"/users/{user_id}")
    else:
        flash("Please enter a new password and confirm it before updating.", "danger")
        return redirect(f"/users/{user_id}")

@app.route("/map/<restaurant_id>")
def show_directions_to_restaurant(restaurant_id):
    """View directions to a particular restaurant."""

    restaurant = crud.get_restaurant_by_id(restaurant_id)

    return render_template("map_directions.html", user=utils.is_logged_in(), restaurant=restaurant)

@app.route("/api/save", methods=["POST"])
def save_favorite_restaurant():
    """Save a favorite restaurant to a user's favorites list."""
    
    restaurant_id = request.json.get("restaurantId")

    try:
        user = crud.get_user_by_id(session["user"])
        user_favorites_list = user.favorites_lists[0]
        restaurant = crud.get_restaurant_by_id(restaurant_id)
        favorite = crud.create_favorite(user, user_favorites_list, restaurant)

        db.session.add(favorite)
        db.session.commit() 
    except Exception as e:
        db.session.rollback()
        print(e)

        return jsonify({
            "success": False,
            "status": f"{restaurant.name} has already been saved to {user_favorites_list.name}!"
        }) 
    
    return jsonify({
            "success": True,
            "status": f"{restaurant.name} saved to {user_favorites_list.name}!"
        })

@app.route("/api/delete-list", methods=["POST"])
def delete_user_favorites_list():
    """Delete a particular Favorites list for a particular user."""

    list_id = request.json.get("listId")

    try:
        favorites_list = crud.get_user_favorites_list_by_id(list_id)

        db.session.delete(favorites_list)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)

        return jsonify({
            "success": False,
            "status": "Error. List not deleted."
        })

    return jsonify({
        "success": True,
        "status": f"{favorites_list.name} deleted.",
        "data": {
            "listId": list_id
        }
    })

@app.route("/api/delete-favorite", methods=["POST"])
def delete_favorite_restaurant():
    """Delete, or unfavorite, a restaurant for a user."""

    favorite_id = request.json.get("favoriteId")

    try:
        favorite = crud.get_favorite_by_id(favorite_id)

        db.session.delete(favorite)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)

        return jsonify({
            "success": False,
            "status": f"Error. Favorite not deleted."
        })

    return jsonify({
        "success": True,
        "status": f"Favorite deleted successfully.",
        "data": {
            "favoriteId": favorite_id
        }
    })

@app.route("/api/delete-review", methods=["POST"])
def delete_user_review():
    """Delete a User Review from a particular restaurant."""

    user_review_id = request.json.get("userReviewId")

    try:
        user_review = crud.get_user_review_by_id(user_review_id)

        db.session.delete(user_review)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)

        return jsonify({
            "success": False,
            "status": "User Favorite not deleted."
        })

    return jsonify({
        "success": True,
        "status": "User Review deleted successfully."
    })

@app.route("/api/restaurants", methods=["POST"])
def get_restaurant_information():
    """Get searched restaurants' information."""

    restaurant_locations = []
    restaurants = request.json.get("restaurants")

    for restaurant in restaurants:
        restaurant = crud.get_restaurant_by_id(restaurant["restaurantId"])

        restaurant_info = {
            "restaurantId": restaurant.restaurant_id,
            "name": restaurant.name,
            "rating": restaurant.rating,
            "address": {
                "street": restaurant.street_address,
                "city": restaurant.city,
                "state": restaurant.state,
                "zipcode": restaurant.zipcode
            },
            "latitude": restaurant.latitude,
            "longitude": restaurant.longitude
        }

        restaurant_locations.append(restaurant_info)

    return jsonify(restaurant_locations)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)