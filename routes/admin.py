
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.student import Student
from models.faculty import Faculty
from models.department import Department
from models.subject import Subject
from models.assignment import Assignment
from models.notice import Notice


admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "admin":
        return "Access denied!", 403

    total_students = Student.query.count()
    total_faculty = Faculty.query.count()
    total_departments = Department.query.count()
    total_subjects = Subject.query.count()
    total_assignments = Assignment.query.count()
    total_notices = Notice.query.count()

    return render_template(
        "admin/dashboard.html",
        total_students=total_students,
        total_faculty=total_faculty,
        total_departments=total_departments,
        total_subjects=total_subjects,
        total_assignments=total_assignments,
        total_notices=total_notices
    )
