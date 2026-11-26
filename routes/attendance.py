
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from models import db
from models.attendance import Attendance
from models.student import Student
from models.subject import Subject
from sqlalchemy import func

attendance = Blueprint(
    "attendance",
    __name__,
    url_prefix="/admin/attendance"
)

def admin_required():
    return current_user.is_authenticated and current_user.role == "admin"


@attendance.route("/")
@login_required
def view_attendance():
    if not admin_required():
        return "Access Denied!", 403

    records = Attendance.query.order_by(Attendance.date.desc()).all()

    return render_template(
        "admin/attendance.html",
        records=records
    )


@attendance.route("/mark", methods=["GET", "POST"])
@login_required
def mark_attendance():
    if not admin_required():
        return "Access Denied!", 403

    students = Student.query.all()
    subjects = Subject.query.all()

    if request.method == "POST":
        student_id = request.form.get("student_id")
        subject_id = request.form.get("subject_id")
        date_value = request.form.get("date")
        status = request.form.get("status")
        remarks = request.form.get("remarks", "").strip()

        if not student_id or not subject_id or not date_value:
            flash("Please fill all required fields.")
            return redirect(url_for("attendance.mark_attendance"))

        attendance_date = datetime.strptime(date_value, "%Y-%m-%d").date()

        existing = Attendance.query.filter_by(
            student_id=int(student_id),
            subject_id=int(subject_id),
            date=attendance_date
        ).first()

        if existing:
            flash("Attendance for this student, subject and date already exists.")
            return redirect(url_for("attendance.mark_attendance"))

        record = Attendance(
            student_id=int(student_id),
            subject_id=int(subject_id),
            date=attendance_date,
            status=status,
            remarks=remarks
        )

        db.session.add(record)
        db.session.commit()

        flash("Attendance marked successfully!")
        return redirect(url_for("attendance.view_attendance"))

    return render_template(
        "admin/mark_attendance.html",
        students=students,
        subjects=subjects
    )

@attendance.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_attendance(id):
    if not admin_required():
        return "Access Denied!", 403

    record = Attendance.query.get_or_404(id)
    students = Student.query.all()
    subjects = Subject.query.all()

    if request.method == "POST":
        student_id = request.form.get("student_id")
        subject_id = request.form.get("subject_id")
        date_value = request.form.get("date")
        status = request.form.get("status")

        if not student_id or not subject_id or not date_value:
            flash("Please fill all required fields.")
            return redirect(url_for("attendance.edit_attendance", id=id))

        attendance_date = datetime.strptime(
            date_value, "%Y-%m-%d"
        ).date()

        duplicate = Attendance.query.filter(
            Attendance.id != id,
            Attendance.student_id == int(student_id),
            Attendance.subject_id == int(subject_id),
            Attendance.date == attendance_date
        ).first()

        if duplicate:
            flash("Attendance already exists for this student, subject and date.")
            return redirect(url_for("attendance.edit_attendance", id=id))

        record.student_id = int(student_id)
        record.subject_id = int(subject_id)
        record.date = attendance_date
        record.status = status
        record.remarks = request.form.get("remarks", "").strip()

        db.session.commit()

        flash("Attendance updated successfully!")
        return redirect(url_for("attendance.view_attendance"))

    return render_template(
        "admin/edit_attendance.html",
        record=record,
        students=students,
        subjects=subjects
    )


@attendance.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_attendance(id):
    if not admin_required():
        return "Access Denied!", 403

    record = Attendance.query.get_or_404(id)

    db.session.delete(record)
    db.session.commit()

    flash("Attendance deleted successfully!")
    return redirect(url_for("attendance.view_attendance"))

@attendance.route("/report")
@login_required
def attendance_report():
    if not admin_required():
        return "Access Denied!", 403

    students = Student.query.all()
    report = []

    for student in students:
        total = Attendance.query.filter_by(
            student_id=student.id
        ).count()

        present = Attendance.query.filter(
            Attendance.student_id == student.id,
            Attendance.status.in_(["Present", "Late"])
        ).count()

        absent = Attendance.query.filter_by(
            student_id=student.id,
            status="Absent"
        ).count()

        percentage = (present / total * 100) if total > 0 else 0

        report.append({
            "student": student,
            "total": total,
            "present": present,
            "absent": absent,
            "percentage": round(percentage, 2)
        })

    return render_template(
        "admin/attendance_report.html",
        report=report
    )
