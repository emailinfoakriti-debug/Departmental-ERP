
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.faculty import Faculty


faculty = Blueprint("faculty", __name__, url_prefix="/admin/faculty")


def admin_required():
    return current_user.is_authenticated and current_user.role == "admin"


# View all faculty
@faculty.route("/")
@login_required
def view_faculty():

    if not admin_required():
        return "Access Denied!", 403

    all_faculty = Faculty.query.all()

    return render_template(
        "admin/faculty.html",
        faculty_list=all_faculty
    )


# Add faculty
@faculty.route("/add", methods=["GET", "POST"])
@login_required
def add_faculty():

    if not admin_required():
        return "Access Denied!", 403

    if request.method == "POST":

        faculty_id = request.form.get("faculty_id", "").strip()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not all([faculty_id, name, email]):
            flash("Please fill all required fields.")
            return redirect(url_for("faculty.add_faculty"))

        existing = Faculty.query.filter(
            (Faculty.faculty_id == faculty_id) |
            (Faculty.email == email)
        ).first()

        if existing:
            flash("Faculty ID or email already exists.")
            return redirect(url_for("faculty.add_faculty"))

        new_faculty = Faculty(
            faculty_id=faculty_id,
            name=name,
            email=email,
            phone=request.form.get("phone", "").strip(),
            department=request.form.get("department", "").strip(),
            designation=request.form.get("designation", "").strip(),
            qualification=request.form.get("qualification", "").strip()
        )

        db.session.add(new_faculty)
        db.session.commit()

        flash("Faculty added successfully!")

        return redirect(url_for("faculty.view_faculty"))

    return render_template("admin/add_faculty.html")

@faculty.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_faculty(id):

    if not admin_required():
        return "Access Denied!", 403

    member = Faculty.query.get_or_404(id)

    if request.method == "POST":

        faculty_id = request.form.get("faculty_id", "").strip()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not all([faculty_id, name, email]):
            flash("Please fill all required fields.")
            return redirect(url_for("faculty.edit_faculty", id=id))

        duplicate = Faculty.query.filter(
            Faculty.id != id,
            (Faculty.faculty_id == faculty_id) |
            (Faculty.email == email)
        ).first()

        if duplicate:
            flash("Faculty ID or email already exists.")
            return redirect(url_for("faculty.edit_faculty", id=id))

        member.faculty_id = faculty_id
        member.name = name
        member.email = email
        member.phone = request.form.get("phone", "").strip()
        member.department = request.form.get("department", "").strip()
        member.designation = request.form.get("designation", "").strip()
        member.qualification = request.form.get("qualification", "").strip()

        db.session.commit()

        flash("Faculty updated successfully!")
        return redirect(url_for("faculty.view_faculty"))

    return render_template(
        "admin/edit_faculty.html",
        member=member
    )

@faculty.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_faculty(id):

    if not admin_required():
        return "Access Denied!", 403

    member = Faculty.query.get_or_404(id)

    db.session.delete(member)
    db.session.commit()

    flash("Faculty deleted successfully!")

    return redirect(url_for("faculty.view_faculty"))
