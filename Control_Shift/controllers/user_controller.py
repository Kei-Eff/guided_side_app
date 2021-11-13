from flask import Blueprint, request, render_template, redirect, url_for, abort
from main import db, lm
from models.users import User
from schemas.user_schema import user_schema, multi_user_schema, user_update_schema
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError

@lm.user_loader
def load_user(user):
    return User.query.get(user)

@lm.unauthorized_handler
def unauthorized():
    return redirect('/users/login/')

users = Blueprint("users", __name__)

@users.route("/users/signup/", methods=["GET"])
def get_users():
    """Displays aa list of users from the database"""
    data = {
        "page_title": "User Index",
        "users": multi_user_schema.dump(User.query.all())
    }
    return render_template("user_index.html", page_data=data)

@users.route("/users/signup/", methods=["GET", "POST"])
def sign_up():
    """Displays the signup form/creates a new user when the form is submitted"""
    data = {"page_title": "Sign Up"}

    if request.method == "GET":
        return render_template("signup.html", page_data=data)

    new_user = user_schema.load(request.form)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for("users.get_users"))

@users.route("/users/login/", methods=["GET", "POST"])
def log_in():
    data = {"page_title": "Log In"}

    if request.method == "GET":
        return render_template("login.html", page_data = data)

    user = user.query.filter_by(email=request.form["email"]).first()
    if user and user.check_password(password=request.form["password"]):
        login_user(user)
        return redirect(url_for("keyboards.get_keyboards"))
        
    abort(401, "Login unsuccessful. Did you supply the correct username and password?")