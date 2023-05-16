"""CRUD operations for Foodie Friend app."""

from model import (db, User, Restaurant, YelpReview, UserReview, 
                   Image, UserFavoritesList, Favorite, connect_to_db)
from datetime import datetime

def create_user(fname, lname, email, password):
    """Create and return a new User."""

    user = User(fname=fname, lname=lname, email=email, 
                password=password, created_at=datetime.now())

    return user

def get_user_by_email(email):
    """Get a user by email."""

    return User.query.filter(User.email == email).first()

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

def create_favorite(user, user_favorites_list, restaurant):
    """Create and return a new Favorite."""

    favorite = Favorite(restaurant=restaurant, 
                        user_favorites_list=user_favorites_list, 
                        user=user, created_at=datetime.now())
    
    return favorite


if __name__ == "__main__":
    from server import app
    connect_to_db(app)