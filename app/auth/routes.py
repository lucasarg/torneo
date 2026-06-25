# app/auth/routes.py
# -------------------
# Authentication blueprint:
# - /auth/login     -> user login
# - /auth/register  -> user registration
# - /auth/logout    -> end session

from urllib.parse import urlsplit

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db
from ..models import User
from .forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__)

def _safe_next_url(next_url: str | None) -> str | None:
    """Return next_url only when it is a local path."""
    if not next_url:
        return None
    parsed = urlsplit(next_url)
    if parsed.scheme or parsed.netloc:
        return None
    if not parsed.path.startswith("/"):
        return None
    return next_url

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Authenticate a user by username/password. If already authenticated,
    redirect to dashboard. On success, redirect to a safe 'next' path or dashboard.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Login successful", "success")
            next_url = _safe_next_url(request.args.get("next"))
            return redirect(next_url or url_for("main.dashboard"))

        flash("Invalid username or password", "danger")

    return render_template("login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user. If already authenticated, redirect to dashboard.
    On success, logs the user in and redirects to dashboard.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip()

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists", "warning")
        else:
            user = User(username=username, email=email)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash("Account created successfully", "success")
            return redirect(url_for("main.dashboard"))

    return render_template("register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """
    End the current session and return to home.
    """
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("main.home"))