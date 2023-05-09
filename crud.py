"""CRUD operations for Foodie Friend app."""

from model import (db, User, Restaurant, YelpReview, UserReview, 
                   Image, UserFavoritesList, Favorite, connect_to_db)



if __name__ == "__main__":
    from server import app
    connect_to_db(app)