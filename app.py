"""Blogly application."""

from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "1234"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    """redirects to list of users"""
    return redirect("/posts")

@app.route('/users')
def list_users():
    """Show list of all users in DB"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('index.html', users=users)

@app.route('/users/new', methods=['GET'])
def make_new_user():
    """Show user form to submit new user"""
    return render_template('users/new_user_form.html')

@app.route('/users/new', methods = ["POST"])
def create_user():
    """form submit to create new user"""
    first_name = request.form['first_name'].capitalize()
    last_name = request.form['last_name'].capitalize()
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
    """delete existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

#routes for posts

@app.route('/posts')
def list_posts():
    """Show all posts"""

    posts=Post.query.all()
    return render_template('posts/posts.html', posts=posts)

@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def make_new_post(user_id):
    """show post form to create new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/new_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    """submit post form to create new post"""

    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    new_post = Post(title=title, content=content, user=user, tags=tags)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """show a post"""
    post = Post.query.get_or_404(post_id)

    return render_template("posts/post_details.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def edit_post(post_id):
    """show form to edit a post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("posts/edit_post.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods = ['POST'])
def update_post(post_id):
    """update post using the edit post form"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["edit_post_title"]
    post.content = request.form["edit_post_content"]
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete', methods = ['POST'])
def delete_post(post_id):
    """delete existing post"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

# routes for tags

@app.route('/tags')
def list_tags():
    """list all tags, with links to tag detail page"""

    tags = Tag.query.all()
    return render_template('tags/list_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """show details of a tag, have links to edit and delete"""
    tag = Tag.query.get_or_404(tag_id)

    return render_template("tags/tag_details.html", tag=tag)

@app.route('/tags/new')
def make_new_tag():
    """show form to create new tag"""
    return render_template('tags/new_tag.html')

@app.route('/tags/new', methods=['POST'])
def create_tag():
    """submit form for new tag, creates tag, redirect to tag list"""
    
    name = request.form['tag_name']

    if "name" in session:
        return redirect("/tags")

    else:
        new_tag = Tag(name = name)
        db.session.add(new_tag)
        db.session.commit()
        return redirect("/tags")

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """show form to edit a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tags/edit_tag.html", tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def update_tag(tag_id):
    """submit form, update tag, redirects to tag list"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["edit_tag_name"]

    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """deletes tag, redirects to tag list"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")



    
