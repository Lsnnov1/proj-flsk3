"""Blogly application."""
from flask import Flask, request, render_template, redirect, url_for, flash
from models import db, connect_db, User, Post, Tag
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

# User Routes
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

# Post Routes
@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def new_post_form(user_id):
    """Show form to add a post for that user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("newpost.html", user=user, tags=tags)

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
    tags = Tag.query.all()
    return render_template("edit_post.html", post=post, user=user, tags=tags)

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

# Tag Routes
@app.route('/tags')
def tags_index():
    """Show a page with info on all tags"""
    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

@app.route('/tags/new', methods=["GET"])
def tags_new_form():
    """Show a form to create a new tag"""
    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)

@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")
    return redirect("/tags")

@app.route('/tags/<int:tag_id>', methods=["GET"])
def tags_show(tag_id):
    """Show a page with info on a specific tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")
    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")
    return redirect("/tags")

if __name__ == "__main__":
    app.run(debug=True)