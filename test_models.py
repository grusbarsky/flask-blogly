from unittest import TestCase

from app import app
from models import db, Users, Posts

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests for model of Users"""
    def setUp(self):
        """clean up any exisiting users"""

        User.query.delete()

    def tearDown(self):
        """clean up any failed transaction"""

        db.session.rollback()
    
    def test_list_users(self):
        url = 'https://www.looper.com/img/gallery/things-only-adults-notice-in-alice-in-wonderland/intro-1602781527.jpg'
        user = User(first_name="Alice", last_name='Wonderland', image_url= url )

        db.session.add(user)
        db.session.commit()

        users = User.list_users()
        self assertEquals(users, [user])

class PostModelTestCase(TestCase):
    """Tests for model of Users"""
    def setUp(self):
        """clean up any exisiting users"""

        Post.query.delete()

    def tearDown(self):
        """clean up any failed transaction"""

        db.session.rollback()
