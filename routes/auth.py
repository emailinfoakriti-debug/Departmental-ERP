
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for("admin.dashboard"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):

            if user.status != "Active":
                flash("Your account is inactive.")
                return redirect(url_for("auth.login"))

            login_user(user)

            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))

            elif user.role == "faculty":
                  return redirect(url_for("faculty_portal.dashboard"))

            elif user.role == "student":
                return redirect(url_for("student_portal.dashboard"))
                logout_user()
                flash("Invalid user role.")
        else:
            flash("Invalid username or password.")

    return render_template("auth/login.html")


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have logged out successfully.")

    return redirect(url_for("auth.login"))
