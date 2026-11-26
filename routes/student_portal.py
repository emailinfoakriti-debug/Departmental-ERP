
from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from models.student import Student
from models.attendance import Attendance
from models.marks import Marks
from models.notice import Notice
from models.timetable import Timetable
from models.assignment import Assignment

student_portal = Blueprint(
    "student_portal",
    __name__,
    url_prefix="/student"
)


@student_portal.route("/dashboard")
@login_required

def attendance():

    if current_user.role != "student":
        abort(403)

    student = Student.query.filter_by(
        email=current_user.email
    ).first()

    if not student:
        return "Student record not found.", 404

    records = Attendance.query.filter_by(
        student_id=student.id
    ).all()

    return render_template(
        "student/attendance.html",
        student=student,
        records=records
    )

@student_portal.route("/marks")
@login_required
def marks():

    if current_user.role != "student":
        abort(403)

    student = Student.query.filter_by(
        email=current_user.email
    ).first()

    if not student:
        return "Student record not found.", 404

    marks_records = Marks.query.filter_by(
        student_id=student.id
    ).all()

    return render_template(
        "student/marks.html",
        student=student,
        marks_records=marks_records
    )

from models.notice import Notice

@student_portal.route("/notices")
@login_required
def notices():

    if current_user.role != "student":
        abort(403)

    student = Student.query.filter_by(
        email=current_user.email
    ).first()

    if not student:
        return "Student record not found.", 404

    notices_list = Notice.query.order_by(
        Notice.publish_date.desc()
    ).all()

    return render_template(
        "student/notices.html",
        student=student,
        notices_list=notices_list
    )

@student_portal.route("/timetable")
@login_required
def timetable():

    if current_user.role != "student":
        abort(403)

    student = Student.query.filter_by(
        email=current_user.email
    ).first()

    if not student:
        return "Student record not found.", 404

    timetable_records = Timetable.query.filter_by(
        semester=student.semester,
        section=student.section
    ).all()

    return render_template(
        "student/timetable.html",
        student=student,
        timetable_records=timetable_records
    )
@student_portal.route("/assignments")
@login_required
def assignments():

    if current_user.role != "student":
        abort(403)

    student = Student.query.filter_by(
        email=current_user.email
    ).first()

    if not student:
        return "Student record not found.", 404

    assignments_list = Assignment.query.order_by(
        Assignment.due_date.asc()
    ).all()

    return render_template(
        "student/assignments.html",
        student=student,
        assignments_list=assignments_list
    )