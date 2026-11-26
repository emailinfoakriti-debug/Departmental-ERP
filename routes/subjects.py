
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.subject import Subject
from models.department import Department

subjects = Blueprint(
    "subjects",
    __name__,
    url_prefix="/admin/subjects"
)

def admin_required():
    return current_user.is_authenticated and current_user.role == "admin"


@subjects.route("/")
@login_required
def view_subjects():
    if not admin_required():
        return "Access Denied!", 403

    subject_list = Subject.query.all()
    return render_template(
        "admin/subjects.html",
        subjects=subject_list
    )


@subjects.route("/add", methods=["GET", "POST"])
@login_required
def add_subject():
    if not admin_required():
        return "Access Denied!", 403

    departments = Department.query.all()

    if request.method == "POST":
        code = request.form.get("subject_code", "").strip()
        name = request.form.get("subject_name", "").strip()

        if not code or not name:
            flash("Subject code and name are required.")
            return redirect(url_for("subjects.add_subject"))

        existing = Subject.query.filter_by(subject_code=code).first()
        if existing:
            flash("Subject code already exists.")
            return redirect(url_for("subjects.add_subject"))

        new_subject = Subject(
            subject_code=code,
            subject_name=name,
            semester=int(request.form.get("semester")),
            credits=int(request.form.get("credits", 4)),
            department_id=int(request.form.get("department_id"))
                if request.form.get("department_id") else None
        )

        db.session.add(new_subject)
        db.session.commit()

        flash("Subject added successfully!")
        return redirect(url_for("subjects.view_subjects"))

    return render_template(
        "admin/add_subject.html",
        departments=departments
    )

@subjects.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_subject(id):
    if not admin_required():
        return "Access Denied!", 403

    subject = Subject.query.get_or_404(id)
    departments = Department.query.all()

    if request.method == "POST":
        code = request.form.get("subject_code", "").strip()
        name = request.form.get("subject_name", "").strip()

        if not code or not name:
            flash("Subject code and name are required.")
            return redirect(url_for("subjects.edit_subject", id=id))

        duplicate = Subject.query.filter(
            Subject.id != id,
            Subject.subject_code == code
        ).first()

        if duplicate:
            flash("Subject code already exists.")
            return redirect(url_for("subjects.edit_subject", id=id))

        subject.subject_code = code
        subject.subject_name = name
        subject.semester = int(request.form.get("semester"))
        subject.credits = int(request.form.get("credits", 4))
        subject.department_id = (
            int(request.form.get("department_id"))
            if request.form.get("department_id") else None
        )

        db.session.commit()
        flash("Subject updated successfully!")
        return redirect(url_for("subjects.view_subjects"))

    return render_template(
        "admin/edit_subject.html",
        subject=subject,
        departments=departments
    )


@subjects.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_subject(id):
    if not admin_required():
        return "Access Denied!", 403

    subject = Subject.query.get_or_404(id)

    db.session.delete(subject)
    db.session.commit()

    flash("Subject deleted successfully!")
    return redirect(url_for("subjects.view_subjects"))
