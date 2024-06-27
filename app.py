"""Blogly application."""
from flask import Flask, request, render_template, redirect, session
from models import db, connect_db, User
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
def show_user():
    firstname = request.form["first_name"]
    lastname = request.form["last_name"]
    imgurl = request.form["img_url"]
    newuser = User(first_name=firstname, last_name=lastname, img_url=imgurl)

    db.session.add(newuser)
    db.session.commit()
    return redirect(f"/users/{newuser.id}")


@app.route("/users/<int:user_id>")
def get_user(user_id):
    """Get user details"""
    user = User.query.get(user_id)
    return render_template("details.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=["GET"])
def edit_user(user_id):
    """Shows form to edit current user"""
    user = User.query.get(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Handle form submission for updating an existing user"""
    user = User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['img_url']

    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Handle form submission for deleting an existing user"""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

if __name__ == "__main__":
    app.run(debug=True)