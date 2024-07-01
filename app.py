"""Blogly application."""
from flask import Flask, request, render_template, redirect, url_for
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "discreetkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.app_context().push()
connect_db(app)
db.create_all()

app.debug = True
debug = DebugToolbarExtension(app)

@app.route("/users")
def show_home():
    """Shows home page"""
    users = User.query.all()
    return render_template("home.html", users=users)

@app.route("/users/create", methods=["GET"])
def create_user_form():
    return render_template("create_user.html")

@app.route("/users", methods=["POST"])
def create_user():
    firstname = request.form["first_name"]
    lastname = request.form["last_name"]
    imgurl = request.form["img_url"]
    newuser = User(first_name=firstname, last_name=lastname, img_url=imgurl)

    db.session.add(newuser)
    db.session.commit()
    return redirect(url_for('get_user', user_id=newuser.id))

@app.route("/users/<int:user_id>")
def get_user(user_id):
    """Get user details"""
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=["GET"])
def edit_user(user_id):
    """Shows form to edit current user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)
    

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Handle form submission for updating an existing user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['img_url']

    db.session.commit()
    return redirect(url_for('show_home'))

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Handle form submission for deleting an existing user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('show_home'))

# New Routes for Posts

@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def new_post_form(user_id):
    """Show form to add a post for that user"""
    user = User.query.get_or_404(user_id)
    return render_template("newpost.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post(user_id):
    """Handle add form; add post and redirect to the post detail page"""
    title = request.form['title']
    content = request.form['content']
    newpost = Post(title=title, content=content, user_id=user_id)

    db.session.add(newpost)
    db.session.commit()
    return redirect(url_for('show_post', post_id=newpost.id))


@app.route("/posts/<int:post_id>", methods=["GET"])
def show_post(post_id):
    """Show a post. Show buttons to edit and delete the post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    return render_template("post.html", post=post, user=user)



@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def edit_post_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    return render_template("edit_post.html", post=post, user=user)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """Handle editing of a post. Redirect back to the post view"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()
    return redirect(url_for('show_post', post_id=post.id))


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete the post"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('get_user', user_id=user_id))

if __name__ == "__main__":
    app.run(debug=True)
