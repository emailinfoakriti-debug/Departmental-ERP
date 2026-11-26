
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.department import Department

department = Blueprint(
    "department",
    __name__,
    url_prefix="/admin/departments"
)


def admin_required():
    return current_user.is_authenticated and current_user.role == "admin"


# View departments
@department.route("/")
@login_required
def view_departments():

    if not admin_required():
        return "Access Denied!", 403

    departments = Department.query.all()

    return render_template(
        "admin/departments.html",
        departments=departments
    )


# Add department
@department.route("/add", methods=["GET", "POST"])
@login_required
def add_department():

    if not admin_required():
        return "Access Denied!", 403

    if request.method == "POST":

        code = request.form.get("department_code", "").strip()
        name = request.form.get("department_name", "").strip()

        if not code or not name:
            flash("Department code and name are required.")
            return redirect(url_for("department.add_department"))

        existing = Department.query.filter(
            (Department.department_code == code) |
            (Department.department_name == name)
        ).first()

        if existing:
            flash("Department code or name already exists.")
            return redirect(url_for("department.add_department"))

        new_department = Department(
            department_code=code,
            department_name=name,
            hod=request.form.get("hod", "").strip(),
            description=request.form.get("description", "").strip(),
            status=request.form.get("status", "Active")
        )

        db.session.add(new_department)
        db.session.commit()

        flash("Department added successfully!")

        return redirect(url_for("department.view_departments"))

    return render_template("admin/add_department.html")

@department.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_department(id):

    if not admin_required():
        return "Access Denied!", 403

    dept = Department.query.get_or_404(id)

    if request.method == "POST":

        code = request.form.get("department_code", "").strip()
        name = request.form.get("department_name", "").strip()

        if not code or not name:
            flash("Department code and name are required.")
            return redirect(url_for("department.edit_department", id=id))

        duplicate = Department.query.filter(
            Department.id != id,
            (Department.department_code == code) |
            (Department.department_name == name)
        ).first()

        if duplicate:
            flash("Department code or name already exists.")
            return redirect(url_for("department.edit_department", id=id))

        dept.department_code = code
        dept.department_name = name
        dept.hod = request.form.get("hod", "").strip()
        dept.description = request.form.get("description", "").strip()
        dept.status = request.form.get("status", "Active")

        db.session.commit()

        flash("Department updated successfully!")

        return redirect(url_for("department.view_departments"))

    return render_template(
        "admin/edit_department.html",
        dept=dept
    )

@department.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_department(id):

    if not admin_required():
        return "Access Denied!", 403

    dept = Department.query.get_or_404(id)

    db.session.delete(dept)
    db.session.commit()

    flash("Department deleted successfully!")

    return redirect(url_for("department.view_departments"))
