
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from datetime import datetime

from models import db
from models.notice import Notice

notices = Blueprint(
    "notices",
    __name__,
    url_prefix="/admin/notices"
)


def admin_required():
    return current_user.is_authenticated and current_user.role == "admin"


@notices.route("/")
@login_required
def view_notices():

    if not admin_required():
        abort(403)

    records = Notice.query.order_by(
        Notice.publish_date.desc()
    ).all()

    return render_template(
        "admin/notices.html",
        records=records
    )


@notices.route("/add", methods=["GET", "POST"])
@login_required
def add_notice():

    if not admin_required():
        abort(403)

    if request.method == "POST":

        try:
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            category = request.form.get("category", "").strip()

            publish_date = datetime.strptime(
                request.form.get("publish_date"), "%Y-%m-%d"
            ).date()

            expiry_value = request.form.get("expiry_date")

            expiry_date = (
                datetime.strptime(expiry_value, "%Y-%m-%d").date()
                if expiry_value else None
            )

            if not title or not description:
                flash("Title and description are required.")
                return redirect(url_for("notices.add_notice"))

            if expiry_date and expiry_date < publish_date:
                flash("Expiry date cannot be before publish date.")
                return redirect(url_for("notices.add_notice"))

            new_notice = Notice(
                title=title,
                description=description,
                category=category,
                publish_date=publish_date,
                expiry_date=expiry_date
            )

            db.session.add(new_notice)
            db.session.commit()

            flash("Notice published successfully!")

            return redirect(url_for("notices.view_notices"))

        except (ValueError, TypeError):
            db.session.rollback()
            flash("Please enter valid notice details.")

    return render_template("admin/add_notice.html")


@notices.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_notice(id):

    if not admin_required():
        abort(403)

    record = Notice.query.get_or_404(id)

    if request.method == "POST":

        try:
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            category = request.form.get("category", "").strip()

            publish_date = datetime.strptime(
                request.form.get("publish_date"), "%Y-%m-%d"
            ).date()

            expiry_value = request.form.get("expiry_date")

            expiry_date = (
                datetime.strptime(expiry_value, "%Y-%m-%d").date()
                if expiry_value else None
            )

            if not title or not description:
                flash("Title and description are required.")
                return redirect(url_for("notices.edit_notice", id=id))

            if expiry_date and expiry_date < publish_date:
                flash("Expiry date cannot be before publish date.")
                return redirect(url_for("notices.edit_notice", id=id))

            record.title = title
            record.description = description
            record.category = category
            record.publish_date = publish_date
            record.expiry_date = expiry_date

            db.session.commit()

            flash("Notice updated successfully!")

            return redirect(url_for("notices.view_notices"))

        except (ValueError, TypeError):
            db.session.rollback()
            flash("Please enter valid notice details.")

    return render_template(
        "admin/edit_notice.html",
        record=record
    )


@notices.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_notice(id):

    if not admin_required():
        abort(403)

    record = Notice.query.get_or_404(id)

    db.session.delete(record)
    db.session.commit()

    flash("Notice deleted successfully!")

    return redirect(url_for("notices.view_notices"))
