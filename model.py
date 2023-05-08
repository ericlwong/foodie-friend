from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.model):
    """Data model for a user."""


class Restaurant(db.model):
    """Data model for a restaurant."""


class Review(db.model):
    """Data model for a review."""


class Image(db.model):
    """Data model for a food/restaurant image."""


class Favorite(db.model):
    """Data model for a user-favorited restaurant."""


class Search(db.model):
    """Data model for a restaurant/food search query."""


class UserFavoritesList(db.model):
    """Data model for a user's favorites list."""


def connect_to_db(flask_app, db_uri = "postgresql:///foodies", echo = True):
    """Connect the database to our Flask app."""

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to db!")

# if __name__ == "__main__":
#     from server import app

#     connect_to_db(app)