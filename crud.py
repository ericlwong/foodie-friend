"""CRUD operations for Foodie Friend app."""

from model import (db, User, Restaurant, YelpReview, UserReview, 
                   Image, UserFavoritesList, Favorite, connect_to_db)
from datetime import datetime

def create_user(fname, lname, email, password, city, 
                state, zipcode, address, address_2=None):
    """Create and return a new User."""

    user = User(fname=fname, 
                lname=lname, 
                email=email, 
                password=password, 
                address=address, 
                address_2=address_2, 
                city=city, 
                state=state, 
                zipcode=zipcode, 
                created_at=datetime.now())

    return user

def get_users():
    """Get all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Get a user by id."""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Get a user by email."""

    return User.query.filter(User.email == email).first()

def set_user_email(user, new_email):
    """Update a user's email attribute."""

    if new_email and user.email != new_email:
        user.email = new_email

def set_user_password(user, new_pass):
    """Update a user's password attribute."""

    if new_pass and user.password != new_pass:
        user.password = new_pass

def set_user_fname(user, new_fname):
    """Update a user's first name attribute."""

    if new_fname and user.fname != new_fname:
        user.fname = new_fname

def set_user_lname(user, new_lname):
    """Update a user's last name attribute."""

    if new_lname and user.lname != new_lname:
        user.lname = new_lname

def set_user_address(user, new_addr):
    """Update a user's address attribute."""

    if new_addr and user.address != new_addr:
        user.address = new_addr

def set_user_address_2(user, new_addr_2):
    """Update a user's address_2 attribute."""

    if new_addr_2 and user.address_2 != new_addr_2:
        user.address_2 = new_addr_2

def set_user_city(user, new_city):
    """Update a user's city attribute."""

    if new_city and user.city != new_city:
        user.city = new_city

def set_user_state(user, new_state):
    """Update a user's state attribute."""

    if new_state and user.state != new_state:
        user.state = new_state

def set_user_zipcode(user, new_zip):
    """Update a user's zipcode attribute."""

    if new_zip and user.zipcode != new_zip:
        user.zipcode = new_zip

def set_update_at_time(user):
    """Update a user's update_at attribute."""

    user.updated_at = datetime.now()

def create_restaurant(name, rating, street_address, city, state, 
                      zipcode, latitude, longitude, categories,
                      phone_number=None, business_hours=None):
    """Create and return a new Restaurant."""

    restaurant = Restaurant(
                    name=name, 
                    rating=rating, 
                    street_address=street_address, 
                    city=city, 
                    state=state, 
                    zipcode=zipcode,
                    latitude=latitude,
                    longitude=longitude, 
                    categories=categories,
                    phone_number=phone_number, 
                    business_hours=business_hours)
    
    return restaurant

def get_restaurants():
    """Get all restaurants."""

    return Restaurant.query.all()

def get_restaurant_by_id(restaurant_id):
    """Get a restaurant by id."""

    return Restaurant.query.get(restaurant_id)

def get_restaurants_by_term_location(search_term, location):
    """Get all restaurants best matching the search term and location."""

    restaurants = Restaurant.query.filter(
        (Restaurant.city == location) & (
        (db.func.lower(Restaurant.name).like(f"%{search_term}%")) | (Restaurant.categories.has_key(search_term))
        )).all()

    # for restaurant in restaurants:
    #     if search_term in restaurant.categories:
    #         matched_restaurants.add(restaurant
    #                                 )    
    return restaurants

def create_yelp_review(restaurant, body, rating, review_url):
    """Create and return a new Yelp Review."""

    yelp_review = YelpReview(restaurant=restaurant, body=body, 
                             rating=rating, review_url=review_url)
    
    return yelp_review

def create_user_review(user, restaurant, body, rating):
    """Create and return a new User Review."""

    user_review = UserReview(user=user, restaurant=restaurant, 
                             body=body, rating=rating)
    
    return user_review

def create_image(restaurant, img_url):
    """Create and return a new Image."""

    image = Image(restaurant=restaurant, img_url=img_url)

    return image

def create_user_favorites_list(user, name):
    """Create and return a new User Favorites List."""

    favorites_list = UserFavoritesList(user=user, name=name, 
                                       created_at=datetime.now())

    return favorites_list

def get_user_favorites_list_by_id(list_id):
    """Get a User Favorites List by id."""

    return UserFavoritesList.query.get(list_id)

def create_favorite(user, user_favorites_list, restaurant):
    """Create and return a new Favorite."""

    favorite = Favorite(restaurant=restaurant, 
                        user_favorites_list=user_favorites_list, 
                        user=user, created_at=datetime.now())
    
    return favorite

def get_favorite_by_id(favorite_id):
    """Get a Favorite by id."""

    return Favorite.query.get(favorite_id)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)