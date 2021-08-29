from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# define database columns and fields here
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)  # make sure we do not have users with duplicate emails
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship("Post", backref="user", passive_deletes=True)  # corresponding relationship
    comments = db.relationship("Comment", backref="user", passive_deletes=True)  # corresponding relationship
    likes = db.relationship("Like", backref="user", passive_deletes=True)  # corresponding relationship


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # Cascade means if a user is deleted, all of the posts deleted as well
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    comments = db.relationship("Comment", backref="post", passive_deletes=True)
    likes = db.relationship("Like", backref="post", passive_deletes=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # Cascade means if a user is deleted, all of the posts deleted as well
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
