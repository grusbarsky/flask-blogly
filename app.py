"""Blogly application."""

from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "1234"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    """redirects to list of users"""
    return redirect("/users")

@app.route('/users')
def list_users():
    """Show list of all users in DB"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=['GET'])
def make_new_user():
    """Show user form to submit new user"""
    return render_template('users/new_user_form.html')

@app.route('/users/new', methods = ["POST"])
def create_user():
    """form submit to create new user"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """show details of a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("users/details.html", user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """show edit user form"""
    user = User.query.get_or_404(user_id)
    return render_template("users/edit_user.html", user=user)

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def update_user(user_id):
    """update user using the edit user form"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["edit_first_name"]
    user.last_name = request.form["edit_last_name"]
    user.image_url = request.form["edit_image_url"]

    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    """delete existing user user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")



    
