"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, User, Post, Tag, connect_db
from flask_debugtoolbar import DebugToolbarExtension
import subprocess



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "Testing"
debug = DebugToolbarExtension(app)



try:
    command = "psql -c 'create database blogly'"
    subprocess.call(command, shell = True)
except:
    print(Exception)
    print("Moving on then")


connect_db(app)

with app.app_context():
    db.create_all()



#==================================HOME======================================
@app.route("/")
def root():
    """Redirect to our list of users (To be changed)"""
    return redirect("/posts")


#==================================USERS======================================
@app.route("/users")
def user_list():
    """
    Show all users
    Links to view user details
    Link to new user form
    """
    users = User.query.all()
    return render_template("user_list.html", users = users)


@app.route("/users/new", methods=["GET","POST"])
def user_create():
    if request.method == "GET":
        """Show the add user form"""
        return render_template("user_create.html")
    
    if request.method == "POST":
        """Redirect back to user list upon adding new user"""
        first = request.form['first_name']
        last = request.form['last_name']
        image = request.form['image_url'] or None
        user = User(first_name = first, last_name = last, image_url = image)
        db.session.add(user)
        db.session.commit()
        return redirect("/users", Response= 200)
    
    else:
        return "Error 405 Method Not Allowed"


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """
    Show details for a user
    Links to edit option
    """
    user = User.query.get(user_id)
    posts = Post.query.filter(Post.user_id == user_id)
    return render_template("user_detail.html", user = user, posts= posts )


@app.route("/users/<int:user_id>/edit", methods=["GET","POST"])
def user_edit(user_id):
    user = User.query.get(user_id)
    if request.method == "GET":
        """Allow editing and saving of user information"""
        return render_template("user_edit.html", user = user)
    
    if request.method == "POST":
        """Processes edits and redirects user back to /users page"""
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url'] or None
        db.session.commit()
        return redirect(f"/users/{user_id}", Response= 200)
    
    else:
        return "Error 405 Method Not Allowed"


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def user_delete(user_id):
    """Deletes a user"""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


#==================================POSTS======================================
@app.route("/posts")
def post_list():
    posts = Post.query.all()
    return render_template("post_list.html", posts = posts)

@app.route("/users/<int:user_id>/posts/new",methods=["GET","POST"])
def post_create(user_id):
    user = User.query.get(user_id)
    tags = Tag.query.all()
    if request.method == "GET":
        return render_template("post_create.html", user = user, tags = tags)
    if request.method == "POST":
        tag_ids = [tag_id for tag_id in request.form.getlist("tags")]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        title = request.form.get('title')
        content = request.form.get('content')
        post = Post(title = title, content = content, user_id=user_id, tags = tags)
        db.session.add(post)
        db.session.commit()
        return redirect(f"/users/{user_id}", Response= 200)
    else:
        return "Error 405 Method Not Allowed"


@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    back_url = request.referrer
    post = Post.query.get(post_id)
    user = User.query.get(post.user_id)
    return render_template("post_detail.html", post=post, user=user , back_url = back_url)


@app.route("/posts/<int:post_id>/edit", methods=["GET","POST"])
def post_edit(post_id):
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    if request.method == "GET":
        return render_template("post_edit.html", post=post, tags = tags)
    if request.method == "POST":
        tag_ids = [tag_id for tag_id in request.form.getlist("tags")]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        post.title = request.form['title']
        post.content = request.form['content']
        post.create_at = None
        post.tags = tags
        db.session.commit()
        return redirect(f"/posts/{post_id}", Response= 200)
    else:
        return "Error 405 Method Not Allowed"
    

@app.route("/posts/<int:post_id>/delete",methods=["POST"])
def post_delete(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/",Response=200)


#==================================TAGS======================================
@app.route("/tags")
def tag_list():
    """Lists all tags, with links to the tag detail page."""
    tags = Tag.query.all()
    return render_template("tag_list.html", tags = tags)
    
    
@app.route("/tags/<int:tag_id>")
def tag_show(tag_id):
    tag = Tag.query.get(tag_id)
    posts = Post.query.filter(Post.tags.contains(tag)).all()
    """Show details about a tag. Have links to edit form and to delete."""
    return render_template("tag_show.html", tag = tag, posts = posts)
    
    
@app.route("/tags/new", methods=["GET","POST"])
def tag_create():
    if request.method == "GET":
        """Shows a form to add a new tag."""
        return render_template("tag_create.html")
    
    if request.method == "POST":
        """Process add form, adds tag, and redirect to tag list."""
        name = request.form['name'].replace(" ", "")
        tag = Tag(name = name )
        db.session.add(tag)
        db.session.commit()
        return redirect("/tags",Response=200)
    else:
        return "Error 405 Method Not Allowed"
    
    
@app.route("/tags/<int:tag_id>/edit", methods=["GET","POST"])
def tag_edit(tag_id):
    tag = Tag.query.get(tag_id)
    if request.method == "GET":
        """Show edit form for a tag."""
        return render_template("tag_edit.html", tag=tag)
    if request.method == "POST":
        """Process edit form, edit tag, and redirects to the tags list."""
        tag.id = request.form['id'].replace(" ", "")
        db.session.commit()
        return redirect("/tags",Response=200)
    else:
        return "Error 405 Method Not Allowed"
    
    
@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def tag_delete(tag_id):
    """Delete a tag."""
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags",Response=200)