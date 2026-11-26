
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from models.faculty import Faculty
from models.subject import Subject
from models.attendance import Attendance
from models.timetable import Timetable
from models import db


faculty_portal = Blueprint(
    "faculty_portal",
    __name__,
    url_prefix="/faculty"
)


# FACULTY DASHBOARD
@faculty_portal.route("/dashboard")
@login_required
def dashboard():

    if current_user.role != "faculty":
        abort(403)

    faculty = Faculty.query.filter_by(
        email=current_user.email
    ).first()

    if not faculty:
        return "Faculty record not found.", 404

    return render_template(
        "faculty/dashboard.html",
        faculty=faculty
    )


# MY ASSIGNED SUBJECTS
@faculty_portal.route("/subjects")
@login_required
def my_subjects():

    if current_user.role != "faculty":
        abort(403)

    faculty = Faculty.query.filter_by(
        email=current_user.email
    ).first()

    if not faculty:
        return "Faculty record not found.", 404

    subjects = Subject.query.join(
        Timetable,
        Timetable.subject_id == Subject.id
    ).filter(
        Timetable.faculty_id == faculty.id
    ).distinct().all()

    return render_template(
        "faculty/subjects.html",
        faculty=faculty,
        subjects=subjects
    )


# FACULTY ATTENDANCE
@faculty_portal.route("/attendance")
@login_required
def attendance():

    if current_user.role != "faculty":
        abort(403)

    faculty = Faculty.query.filter_by(
        email=current_user.email
    ).first()

    if not faculty:
        return "Faculty record not found.", 404

    assigned_subject_ids = [
        item.subject_id
        for item in Timetable.query.filter_by(
            faculty_id=faculty.id
        ).all()
    ]

    if assigned_subject_ids:
        records = Attendance.query.filter(
            Attendance.subject_id.in_(assigned_subject_ids)
        ).order_by(
            Attendance.date.desc()
        ).all()
    else:
        records = []

    return render_template(
        "faculty/attendance.html",
        faculty=faculty,
        records=records
    )

# FACULTY MARKS MANAGEMENT
@faculty_portal.route("/marks", methods=["GET", "POST"])
@login_required
def marks():

    from flask import request, flash, redirect, url_for
    from models.marks import Marks
    from models.student import Student

    if current_user.role != "faculty":
        abort(403)

    faculty = Faculty.query.filter_by(
        email=current_user.email
    ).first()

    if not faculty:
        return "Faculty record not found.", 404

    assigned_subjects = Subject.query.join(
        Timetable,
        Timetable.subject_id == Subject.id
    ).filter(
        Timetable.faculty_id == faculty.id
    ).distinct().all()

    if request.method == "POST":

        student_id = request.form.get("student_id", type=int)
        subject_id = request.form.get("subject_id", type=int)
        exam_name = request.form.get("exam_name", "").strip()

        if not student_id or not subject_id or not exam_name:
            flash("Please fill all required fields.")
            return redirect(url_for("faculty_portal.marks"))

        if subject_id not in [s.id for s in assigned_subjects]:
            abort(403)

        student = Student.query.get_or_404(student_id)

        existing = Marks.query.filter_by(
            student_id=student_id,
            subject_id=subject_id,
            exam_name=exam_name
        ).first()

        if existing:
            existing.assignment_marks = request.form.get(
                "assignment_marks", type=float
            )
            existing.internal_marks = request.form.get(
                "internal_marks", type=float
            )
            existing.practical_marks = request.form.get(
                "practical_marks", type=float
            )
            existing.total_marks = sum([
                existing.assignment_marks or 0,
                existing.internal_marks or 0,
                existing.practical_marks or 0
            ])
        else:
            new_marks = Marks(
                student_id=student.id,
                subject_id=subject_id,
                exam_name=exam_name,
                assignment_marks=request.form.get(
                    "assignment_marks", type=float
                ),
                internal_marks=request.form.get(
                    "internal_marks", type=float
                ),
                practical_marks=request.form.get(
                    "practical_marks", type=float
                )
            )

            new_marks.total_marks = sum([
                new_marks.assignment_marks or 0,
                new_marks.internal_marks or 0,
                new_marks.practical_marks or 0
            ])

            db.session.add(new_marks)

        db.session.commit()
        flash("Student marks saved successfully!")

        return redirect(url_for("faculty_portal.marks"))

    students = Student.query.all()

    return render_template(
        "faculty/marks.html",
        faculty=faculty,
        subjects=assigned_subjects,
        students=students
    )

# FACULTY ASSIGNMENT MANAGEMENT
@faculty_portal.route("/assignments", methods=["GET", "POST"])
@login_required
def assignments():

    from flask import request, flash, redirect, url_for
    from datetime import datetime
    from models.assignment import Assignment

    if current_user.role != "faculty":
        abort(403)

    faculty = Faculty.query.filter_by(
        email=current_user.email
    ).first()

    if not faculty:
        return "Faculty record not found.", 404

    assigned_subjects = Subject.query.join(
        Timetable,
        Timetable.subject_id == Subject.id
    ).filter(
        Timetable.faculty_id == faculty.id
    ).distinct().all()

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        subject_id = request.form.get("subject_id", type=int)
        due_date_text = request.form.get("due_date", "")
        total_marks = request.form.get("total_marks", type=float)

        if not title or not subject_id or not due_date_text:
            flash("Please fill all required fields.")
            return redirect(url_for("faculty_portal.assignments"))

        if subject_id not in [s.id for s in assigned_subjects]:
            abort(403)

        try:
            due_date = datetime.strptime(
                due_date_text, "%Y-%m-%d"
            ).date()
        except ValueError:
            flash("Please enter a valid due date.")
            return redirect(url_for("faculty_portal.assignments"))

        new_assignment = Assignment(
            title=title,
            description=description,
            subject_id=subject_id,
            faculty_name=faculty.name,
            due_date=due_date,
            total_marks=total_marks if total_marks is not None else 100
        )

        db.session.add(new_assignment)
        db.session.commit()

        flash("Assignment created successfully!")
        return redirect(url_for("faculty_portal.assignments"))

    assignments_list = Assignment.query.order_by(
        Assignment.due_date.asc()
    ).all()

    return render_template(
        "faculty/assignments.html",
        faculty=faculty,
        subjects=assigned_subjects,
        assignments=assignments_list
    )

# FACULTY NOTICES
@faculty_portal.route("/notices")
@login_required
def notices():

    from models.notice import Notice

    if current_user.role != "faculty":
        abort(403)

    faculty = Faculty.query.filter_by(
        email=current_user.email
    ).first()

    if not faculty:
        return "Faculty record not found.", 404

    notice_list = Notice.query.order_by(
        Notice.publish_date.desc()
    ).all()

    return render_template(
        "faculty/notices.html",
        faculty=faculty,
        notices=notice_list
    )
