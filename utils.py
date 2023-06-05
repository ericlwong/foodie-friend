"Helpers for Foodie Friend app."

from flask import session
from datetime import datetime
import crud
import os
import requests
import utils
import model

STATES = {"AK": "Alaska", "AL": "Alabama", "AR": "Arkansas", "AZ": "Arizona", "CA": "California", 
          "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", 
          "HI": "Hawaii", "IA": "Iowa", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", 
          "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "MA": "Massachusetts", "MD": "Maryland", 
          "ME": "Maine", "MI": "Michigan", "MN": "Minnesota", "MO": "Missouri", "MS": "Mississippi", 
          "MT": "Montana", "NC": "North Carolina", "ND": "North Dakota", "NE": "Nebraska", "NH": "New Hampshire", 
          "NJ": "New Jersey", "NM": "New Mexico", "NV": "Nevada", "NY": "New York", "OH": "Ohio",
          "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", 
          "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VA": "Virginia", 
          "VT": "Vermont", "WA": "Washington", "WI": "Wisconsin", "WV": "West Virginia", "WY": "Wyoming"}

yelp_api_headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + os.environ["YELP_API_KEY"]
}

def convert_time_string(time_str):
    """Convert and return time as 12-Hour Format."""

    time_12_hr = datetime.strptime(time_str, "%H%M")
    return time_12_hr.strftime("%I:%M %p")

def clean_business_hours(yelp_business_hours):
    """Clean and return dictionary of business hours."""

    if yelp_business_hours is None:
        return {}

    cleaned_business_hours = [
        { "day": "Monday", "hours": [] },
        { "day": "Tuesday", "hours": [] },
        { "day": "Wednesday", "hours": [] },
        { "day": "Thursday", "hours": [] },
        { "day": "Friday", "hours": [] },
        { "day": "Saturday", "hours": [] },
        { "day": "Sunday", "hours": [] }
    ]

    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    open_hours_dict = yelp_business_hours[0]["open"]

    for day in open_hours_dict:
        day_idx = day["day"]
        start_time = convert_time_string(day["start"])
        end_time = convert_time_string(day["end"])
        
        cleaned_business_hours[day_idx]["hours"].append(f"{start_time} - {end_time}")
    
    return cleaned_business_hours

def is_logged_in():
    """Return user or None depending on whether user is in session."""

    if "user" in session:
        return crud.get_user_by_id(session["user"])
    else:
        return None
    
def convert_yelp_time_to_datetime(yelp_time_str):
    """Convert a Yelp Review's time string to a datetime object."""
    # 2016-08-29 00:41:13
    return datetime.strptime(yelp_time_str, "%Y-%m-%d %H:%M:%S") 

def search_yelp_restaurants(term, location):
    """Call Yelp Fusion's Search Endpoint for more restaurants."""

    payload = {
        "location": location,
        "term": term
    }

    res = requests.get("https://api.yelp.com/v3/businesses/search", headers=yelp_api_headers, params=payload)
    data = res.json()
    businesses = data["businesses"]

    new_restaurants = []

    for business in businesses:
        business_id = business["id"]

        if crud.get_restaurant_by_yelp_business_id(business_id):
            continue

        name = business["name"]
        rating = business["rating"]
        street_address = business["location"]["address1"]
        city = business["location"]["city"]
        state = business["location"]["state"]
        zipcode = business["location"]["zip_code"]
        latitude = business["coordinates"]["latitude"]
        longitude = business["coordinates"]["longitude"]
        phone_number = business["phone"]

        categories = { "restaurants": "Restaurants" }
        for category in business["categories"]:
            categories[category["alias"]] = category["title"]

        # GET request to Yelp endpoint to get business by ID
        business_res = requests.get(f"https://api.yelp.com/v3/businesses/{business_id}", headers=yelp_api_headers)
        business_data = business_res.json()

        business_hours = utils.clean_business_hours(business_data.get("hours", None))
        images = business_data["photos"]

        restaurant = crud.create_restaurant(name, rating, street_address, city, state, zipcode, latitude, 
                                        longitude, categories, business_id, phone_number, business_hours)

        new_restaurants.append(restaurant)
        
        model.db.session.add(restaurant)
        model.db.session.commit()

        # Create Images
        for image_url in images:
            image = crud.create_image(restaurant, image_url)

            model.db.session.add(image)
            model.db.session.commit()

        # Get up to 3 Yelp Reviews for each business
        reviews_res = requests.get(f"https://api.yelp.com/v3/businesses/{business_id}/reviews", headers=yelp_api_headers)
        reviews_data = reviews_res.json()
        reviews = reviews_data["reviews"]

        # Create Yelp Reviews
        for review in reviews:
            reviewer_name = review["user"]["name"]
            review_body = review["text"]
            rating = review["rating"]
            review_url = review["url"]
            yelp_created_date = review["time_created"]
            created_at = utils.convert_yelp_time_to_datetime(yelp_created_date)

            yelp_review = crud.create_yelp_review(restaurant, reviewer_name, review_body, 
                                                  rating, review_url, created_at)

            model.db.session.add(yelp_review)
            model.db.session.commit()

    return new_restaurants