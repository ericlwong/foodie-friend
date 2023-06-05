"""Models for Foodie Friend app."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_json import mutable_json_type
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()


class User(db.Model):
    """Data model for a user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    address_2 = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True, default=None)

    favorites = db.relationship("Favorite", back_populates="user")
    favorites_lists = db.relationship("UserFavoritesList", back_populates="user")
    user_reviews = db.relationship("UserReview", back_populates="user")

    def __repr__(self):
        """Show info about user."""

        return f"<User user_id={self.user_id} fname={self.fname}>"
    

class Restaurant(db.Model):
    """Data model for a restaurant."""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    street_address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    phone_number = db.Column(db.String(12), nullable=True)
    business_hours = db.Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=True)
    categories = db.Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=False)
    yelp_business_id = db.Column(db.String, nullable=False)

    yelp_reviews = db.relationship("YelpReview", back_populates="restaurant")
    user_reviews = db.relationship("UserReview", back_populates="restaurant")
    images = db.relationship("Image", back_populates="restaurant")
    favorites = db.relationship("Favorite", back_populates="restaurant")

    def __repr__(self):
        """Show info about restaurant."""

        return f"<Restaurant restaurant_id={self.restaurant_id} name={self.name}>"
    

class YelpReview(db.Model):
    """Data model for a Yelp Review."""

    __tablename__ = "yelp_reviews"

    yelp_review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.restaurant_id"), nullable=False)
    reviewer_name = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_url = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    restaurant = db.relationship("Restaurant", back_populates="yelp_reviews")

    def __repr__(self):
        """Show info about Yelp Review."""

        return f"<YelpReview yelp_review_id={self.yelp_review_id} rating={self.rating}>"
    

class UserReview(db.Model):
    """Data model for a User Review."""

    __tablename__ = "user_reviews"

    user_review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.restaurant_id"), nullable=False)
    body = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    restaurant = db.relationship("Restaurant", back_populates="user_reviews")
    user = db.relationship("User", back_populates="user_reviews")

    def __repr__(self):
        """Show info about User Review."""

        return f"<UserReview user_review_id={self.user_review_id} rating={self.rating}>"


class Image(db.Model):
    """Data model for a food/restaurant image."""

    __tablename__ = "images"

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.restaurant_id"), nullable=False)
    img_url = db.Column(db.String, nullable=False)

    restaurant = db.relationship("Restaurant", back_populates="images")

    def __repr__(self):
        """Show info about image."""

        return f"<Image image_id={self.image_id} restaurant_id={self.restaurant_id}>"


class UserFavoritesList(db.Model):
    """Data model for a user's favorites list."""

    __tablename__ = "user_favorites_lists"

    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True, default=None)

    user = db.relationship("User", back_populates = "favorites_lists")
    favorites = db.relationship("Favorite", back_populates = "user_favorites_list")

    def __repr__(self):
        """Show info about user's favorites list."""

        return f"<UserFavoritesList list_id={self.list_id} user_id={self.user_id}>"
    

class Favorite(db.Model):
    """Data model for a user-favorited restaurant."""

    __tablename__ = "favorites"

    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    user_favorites_list_id = db.Column(db.Integer, db.ForeignKey("user_favorites_lists.list_id"), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.restaurant_id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    restaurant = db.relationship("Restaurant", back_populates="favorites")
    user = db.relationship("User", back_populates="favorites")
    user_favorites_list = db.relationship("UserFavoritesList", back_populates="favorites")

    __table_args__ = (db.UniqueConstraint("user_id", "user_favorites_list_id", "restaurant_id", 
                                          name="user_favorites_restaurant_idx"),)

    def __repr__(self):
        """Show info about user-favorited restaurant."""

        return f"<Favorite favorite_id={self.favorite_id} restaurant_id={self.restaurant_id} user_id={self.user_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///foodies", echo=True):
    """Connect the database to our Flask app."""

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)