"""Server for Foodie Friend app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
from jinja2 import StrictUndefined
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.app_context().push()


@app.route("/")
def show_homepage():
    """View homepage."""

    return render_template("homepage.html")

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

@app.route("/restaurants")
def show_restaurants():
    """View restaurants."""

    restaurants = crud.get_restaurants()

    return render_template("all_restaurants.html", restaurants=restaurants)

@app.route("/restaurants/<restaurant_id>")
def show_restaurant(restaurant_id):
    """View a particular restaurant."""

    restaurant = crud.get_restaurant_by_id(restaurant_id)
    yelp_reviews = restaurant.yelp_reviews
    images = restaurant.images

    return render_template("restaurant_details.html", restaurant=restaurant, 
                           yelp_reviews=yelp_reviews, images=images)

@app.route("/search")
def search_restaurants():
    """Search for restaurants."""

    query = request.args.get("query")
    location = request.args.get("location")

    restaurants = crud.get_restaurants_by_term_location(query, location)

    return render_template("searched_restaurants.html", restaurants=restaurants, location=location)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)