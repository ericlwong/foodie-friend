"""Script to seed Foodie Friend database."""

import os
import json
import requests
import crud
import model
import server
from random import choice, randint
from datetime import datetime

os.system("dropdb foodies")
os.system("createdb foodies")

model.connect_to_db(server.app)
model.db.create_all()

def convert_time_string(time_str):
    """Convert and return time as 12-Hour Format."""

    time_12_hr = datetime.strptime(time_str, "%H%M")
    return time_12_hr.strftime("%I:%M %p")

def clean_business_hours(yelp_business_hours):
    """Clean and return dictionary of business hours."""

    if yelp_business_hours is None:
        return {}

    cleaned_business_hours = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": []
    }

    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    open_hours_dict = yelp_business_hours[0]["open"]

    for day in open_hours_dict:
        day_idx = day["day"]
        start_time = convert_time_string(day["start"])
        end_time = convert_time_string(day["end"])
        
        cleaned_business_hours[week_days[day_idx]].append(f"{start_time} - {end_time}")
    
    return cleaned_business_hours

# Make initial request to Yelp Business Search endpoint
headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + os.environ["YELP_API_KEY"]
}

payload = {
    "location": "San Francisco",
    "term": "restaurants"
}

res = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=payload)

data = res.json()
businesses = data["businesses"]

restaurants_in_db = []

for business in businesses:
    business_id = business["id"]
    name = business["name"]
    rating = business["rating"]
    street_address = business["location"]["address1"]
    city = business["location"]["city"]
    state = business["location"]["state"]
    zipcode = business["location"]["zip_code"]
    latitude = business["coordinates"]["latitude"]
    longitude = business["coordinates"]["latitude"]
    phone_number = business["phone"]

    categories = { "restaurants": "Restaurants" }
    for category in business["categories"]:
        categories[category["alias"]] = category["title"]

    # GET request to Yelp endpoint to get business by ID
    business_res = requests.get(f"https://api.yelp.com/v3/businesses/{business_id}", headers=headers)
    business_data = business_res.json()

    business_hours = clean_business_hours(business_data.get("hours", None))
    images = business_data["photos"]

    restaurant = crud.create_restaurant(name, rating, street_address, city, state, zipcode, latitude, 
                                        longitude, categories, phone_number, business_hours)
    restaurants_in_db.append(restaurant)

    model.db.session.add(restaurant)
    model.db.session.commit()

    # Create Images
    for image_url in images:
        image = crud.create_image(restaurant, image_url)

        model.db.session.add(image)
        model.db.session.commit()

    # Get up to 3 Yelp Reviews for each business
    reviews_res = requests.get(f"https://api.yelp.com/v3/businesses/{business_id}/reviews", headers=headers)
    reviews_data = reviews_res.json()
    reviews = reviews_data["reviews"]

    # Create Yelp Reviews
    for review in reviews:
        review_body = review["text"]
        rating = review["rating"]
        review_url = review["url"]
        yelp_review = crud.create_yelp_review(restaurant, review_body, rating, review_url)

        model.db.session.add(yelp_review)
        model.db.session.commit()

# Create 10 Users
for n in range(10):
    fname = f"First{n}"
    lname = f"Last{n}"
    email = f"test{n}@test.com"
    password = "test"

    user = crud.create_user(fname, lname, email, password)

    # Create a Favorites List for each user
    list_name = f"{fname}'s List"
    user_favorites_list = crud.create_user_favorites_list(user, list_name)

    # Create a Favorite for each user
    favorite = crud.create_favorite(user, user_favorites_list, choice(restaurants_in_db))
    
    # Create a User Review for each user
    user_review = crud.create_user_review(user, choice(restaurants_in_db), "Review text.", randint(1, 5))

    model.db.session.add_all([user, user_favorites_list, favorite, user_review])
    model.db.session.commit()
