from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "topsecret"  # to encrypt session data
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"  # A database. Tell flask where it is and initialize it.
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment, Like  # these are the tables/columns.

    create_database(app)

    login_manager = LoginManager()  # logs users in/out. They do not have to type in their username and password again
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader  # allows you to access information related to the user from a database given the user id
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("FlaskBlog/" + DB_NAME):
        db.create_all(app=app)  # creates a database if it does not exist
        print("Created database!")
