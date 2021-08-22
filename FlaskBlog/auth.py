from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


# create your routes/pages here
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category="success")
                login_user(user,
                           remember=True)  # login a user using login manager to determine if person logged in or not
                return redirect(url_for('views.home'))
            else:
                flash("Password is incorrect.", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # now check user info
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category="error")
        elif username_exists:
            flash('Username is already in use.', category="error")
        elif password1 != password2:
            flash('Passwords don\'t match', category="error")
        elif len(username) < 2:
            flash('Username is too short.', category="error")
        elif len(password1) < 6:
            flash('Password is too short.', category="error")
        elif len(email) < 4:
            flash('Email is invalid.', category="error")
        else:  # if everything is fine, then new user will be created
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)  # adds new user to the database
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required # you can only access this page if you have been logged in
def logout():
    logout_user()
    return redirect(url_for("views.home"))  # referencing the home function not the route or endpoint
