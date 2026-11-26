
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from datetime import datetime

from models import db
from models.assignment import Assignment
from models.subject import Subject

assignments = Blueprint(
    "assignments",
    __name__,
    url_prefix="/admin/assignments"
)


def admin_required():
    return current_user.is_authenticated and current_user.role == "admin"


@assignments.route("/")
@login_required
def view_assignments():

    if not admin_required():
        abort(403)

    records = Assignment.query.all()

    return render_template(
        "admin/assignments.html",
        records=records
    )


@assignments.route("/add", methods=["GET", "POST"])
@login_required
def add_assignment():

    if not admin_required():
        abort(403)

    subjects = Subject.query.all()

    if request.method == "POST":

        try:
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            subject_id = int(request.form.get("subject_id"))
            faculty_name = request.form.get("faculty_name", "").strip()
            due_date = datetime.strptime(
                request.form.get("due_date"), "%Y-%m-%d"
            ).date()
            total_marks = float(request.form.get("total_marks") or 100)

            if not title:
                flash("Assignment title is required.")
                return redirect(url_for("assignments.add_assignment"))

            if total_marks <= 0:
                flash("Total marks must be greater than zero.")
                return redirect(url_for("assignments.add_assignment"))

            subject = Subject.query.get(subject_id)

            if not subject:
                flash("Please select a valid subject.")
                return redirect(url_for("assignments.add_assignment"))

            new_assignment = Assignment(
                title=title,
                description=description,
                subject_id=subject_id,
                faculty_name=faculty_name,
                due_date=due_date,
                total_marks=total_marks
            )

            db.session.add(new_assignment)
            db.session.commit()

            flash("Assignment added successfully!")

            return redirect(url_for("assignments.view_assignments"))

        except (ValueError, TypeError):
            db.session.rollback()
            flash("Please enter valid assignment details.")

    return render_template(
        "admin/add_assignment.html",
        subjects=subjects
    )


@assignments.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_assignment(id):

    if not admin_required():
        abort(403)

    record = Assignment.query.get_or_404(id)
    subjects = Subject.query.all()

    if request.method == "POST":

        try:
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            subject_id = int(request.form.get("subject_id"))
            faculty_name = request.form.get("faculty_name", "").strip()
            due_date = datetime.strptime(
                request.form.get("due_date"), "%Y-%m-%d"
            ).date()
            total_marks = float(request.form.get("total_marks") or 100)

            if not title or total_marks <= 0:
                flash("Enter a valid title and total marks.")
                return redirect(url_for("assignments.edit_assignment", id=id))

            if not Subject.query.get(subject_id):
                flash("Please select a valid subject.")
                return redirect(url_for("assignments.edit_assignment", id=id))

            record.title = title
            record.description = description
            record.subject_id = subject_id
            record.faculty_name = faculty_name
            record.due_date = due_date
            record.total_marks = total_marks

            db.session.commit()

            flash("Assignment updated successfully!")

            return redirect(url_for("assignments.view_assignments"))

        except (ValueError, TypeError):
            db.session.rollback()
            flash("Please enter valid assignment details.")

    return render_template(
        "admin/edit_assignment.html",
        record=record,
        subjects=subjects
    )


@assignments.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_assignment(id):

    if not admin_required():
        abort(403)

    record = Assignment.query.get_or_404(id)

    db.session.delete(record)
    db.session.commit()

    flash("Assignment deleted successfully!")

    return redirect(url_for("assignments.view_assignments"))
