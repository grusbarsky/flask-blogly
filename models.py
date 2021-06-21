"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, 
                    primary_key = True,
                    autoincrement = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    image_url = db.Column(db.Text, nullable = False)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

class Post(db.Model):
    """Post"""
    __tablename__='posts'

    id = db.Column(db.Integer, 
                    primary_key = True,
                    autoincrement = True)
    title = db.Column(db.String(20), nullable = False)
    content = db.Column(db.String(200), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Tag(db.Model):
    """Tags that can be added to posts"""
    __tablename__='tags'

    id = db.Column(db.Integer, 
                    primary_key = True,
                    autoincrement = True)
    name = db.Column(db.String(15), nullable = False, unique = True)

    posts = db.relationship('Post', secondary="posts_tags", backref="tags")

class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


def connect_db(app):
    """Connect this database to Flask app"""

    db.app = app
    db.init_app(app)