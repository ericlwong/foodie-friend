"""Server for Foodie Friend app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from jinja2 import StrictUndefined
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

    if user and user.email == email and user.password == password:
        session["user"] = email
        flash("Login successful!")

        return redirect("/")
    else:
        flash("Incorrect email and password. Please try again.")

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

    user = crud.get_user_by_email(email)

    if user:
        flash("Email already in use. Please use another one or log in with existing email.")

        return redirect("/signup")
    else:
        new_user = crud.create_user(fname, lname, email, password, city, 
                                state, zipcode, address, address_2)
        
        db.session.add(new_user)
        db.session.commit()

        session["user"] = email
        flash("Account created and logged in!")

        return redirect("/")
    
@app.route("/logout")
def handle_logout():
    """Log user out of account."""

    if "user" in session:
        del session["user"]
        flash("Logged out successfully!") 
    else:
        flash("You are not currently logged in.")

    return redirect("/")

@app.route("/users")
def show_users():
    """View users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users, user=utils.is_logged_in())

@app.route("/users/<user_id>")
def show_user_profile(user_id):
    """View a particular user's profile."""

    user = crud.get_user_by_id(user_id)

    # Can only access the logged-in user's profile
    if "user" in session and user.email == session["user"]:
        return render_template("profile.html", user=user, states=utils.STATES)
    else:
        return redirect("/")

@app.route("/restaurants")
def show_restaurants():
    """View restaurants."""

    restaurants = crud.get_restaurants()

    return render_template("all_restaurants.html", restaurants=restaurants, user=utils.is_logged_in())

@app.route("/restaurants/<restaurant_id>")
def show_restaurant(restaurant_id):
    """View a particular restaurant."""

    restaurant = crud.get_restaurant_by_id(restaurant_id)
    yelp_reviews = restaurant.yelp_reviews
    images = restaurant.images

    return render_template("restaurant_details.html", restaurant=restaurant, 
                           yelp_reviews=yelp_reviews, images=images, user=utils.is_logged_in())

@app.route("/search")
def search_restaurants():
    """Search for restaurants."""

    query = request.args.get("query")
    location = request.args.get("location")

    restaurants = crud.get_restaurants_by_term_location(query, location)

    return render_template("searched_restaurants.html", restaurants=restaurants, 
                           location=location, user=utils.is_logged_in())

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)