
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from models import db
from models.marks import Marks
from models.student import Student
from models.subject import Subject

marks = Blueprint("marks", __name__, url_prefix="/admin/marks")


def admin_required():
    return current_user.is_authenticated and current_user.role == "admin"


@marks.route("/")
@login_required
def view_marks():
    if not admin_required():
        abort(403)

    records = Marks.query.all()

    return render_template("admin/marks.html", records=records)


@marks.route("/add", methods=["GET", "POST"])
@login_required
def add_marks():
    if not admin_required():
        abort(403)

    students = Student.query.all()
    subjects = Subject.query.all()

    if request.method == "POST":
        try:
            student_id = int(request.form.get("student_id"))
            subject_id = int(request.form.get("subject_id"))

            exam_name = request.form.get("exam_name", "").strip()

            assignment = float(request.form.get("assignment_marks") or 0)
            internal = float(request.form.get("internal_marks") or 0)
            practical = float(request.form.get("practical_marks") or 0)

            if not exam_name:
                flash("Please enter the exam name.")
                return redirect(url_for("marks.add_marks"))

            if min(assignment, internal, practical) < 0:
                flash("Marks cannot be negative.")
                return redirect(url_for("marks.add_marks"))

            if not Student.query.get(student_id) or not Subject.query.get(subject_id):
                flash("Please select a valid student and subject.")
                return redirect(url_for("marks.add_marks"))

            total = assignment + internal + practical

            record = Marks(
                student_id=student_id,
                subject_id=subject_id,
                exam_name=exam_name,
                assignment_marks=assignment,
                internal_marks=internal,
                practical_marks=practical,
                total_marks=total
            )

            db.session.add(record)
            db.session.commit()

            flash("Marks added successfully!")
            return redirect(url_for("marks.view_marks"))

        except (ValueError, TypeError):
            db.session.rollback()
            flash("Please enter valid marks.")

    return render_template(
        "admin/add_marks.html",
        students=students,
        subjects=subjects
    )


@marks.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_marks(id):
    if not admin_required():
        abort(403)

    record = Marks.query.get_or_404(id)

    students = Student.query.all()
    subjects = Subject.query.all()

    if request.method == "POST":
        try:
            student_id = int(request.form.get("student_id"))
            subject_id = int(request.form.get("subject_id"))

            exam_name = request.form.get("exam_name", "").strip()

            assignment = float(request.form.get("assignment_marks") or 0)
            internal = float(request.form.get("internal_marks") or 0)
            practical = float(request.form.get("practical_marks") or 0)

            if not exam_name:
                flash("Please enter the exam name.")
                return redirect(url_for("marks.edit_marks", id=id))

            if min(assignment, internal, practical) < 0:
                flash("Marks cannot be negative.")
                return redirect(url_for("marks.edit_marks", id=id))

            if not Student.query.get(student_id) or not Subject.query.get(subject_id):
                flash("Please select a valid student and subject.")
                return redirect(url_for("marks.edit_marks", id=id))

            record.student_id = student_id
            record.subject_id = subject_id
            record.exam_name = exam_name
            record.assignment_marks = assignment
            record.internal_marks = internal
            record.practical_marks = practical
            record.total_marks = assignment + internal + practical

            db.session.commit()

            flash("Marks updated successfully!")
            return redirect(url_for("marks.view_marks"))

        except (ValueError, TypeError):
            db.session.rollback()
            flash("Please enter valid marks.")

    return render_template(
        "admin/edit_marks.html",
        record=record,
        students=students,
        subjects=subjects
    )


@marks.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_marks(id):
    if not admin_required():
        abort(403)

    record = Marks.query.get_or_404(id)

    db.session.delete(record)
    db.session.commit()

    flash("Marks deleted successfully!")

    return redirect(url_for("marks.view_marks"))
