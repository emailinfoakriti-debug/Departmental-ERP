
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models import db
from models.timetable import Timetable
from models.subject import Subject
from models.faculty import Faculty

timetable = Blueprint(
    "timetable",
    __name__,
    url_prefix="/admin/timetable"
)


def admin_required():
    if current_user.role != "admin":
        abort(403)


# 1. View all timetable entries
@timetable.route("/")
@login_required
def view_timetable():
    admin_required()

    entries = Timetable.query.order_by(
        Timetable.semester,
        Timetable.day,
        Timetable.start_time
    ).all()

    return render_template(
        "admin/timetable.html",
        entries=entries
    )


# 2. Add timetable entry
@timetable.route("/add", methods=["GET", "POST"])
@login_required
def add_timetable():
    admin_required()

    subjects = Subject.query.all()
    faculties = Faculty.query.all()

    if request.method == "POST":
        semester = request.form.get("semester")
        section = request.form.get("section")
        subject_id = request.form.get("subject_id")
        faculty_id = request.form.get("faculty_id")
        day = request.form.get("day")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        room = request.form.get("room")

        if not all([
            semester, section, subject_id, faculty_id,
            day, start_time, end_time
        ]):
            flash("Please fill all required fields.", "danger")
            return redirect(url_for("timetable.add_timetable"))

        if start_time >= end_time:
            flash("End time must be later than start time.", "danger")
            return redirect(url_for("timetable.add_timetable"))

        entry = Timetable(
            semester=int(semester),
            section=section,
            subject_id=int(subject_id),
            faculty_id=int(faculty_id),
            day=day,
            start_time=start_time,
            end_time=end_time,
            room=room
        )

        db.session.add(entry)
        db.session.commit()

        flash("Timetable entry added successfully!", "success")
        return redirect(url_for("timetable.view_timetable"))

    return render_template(
        "admin/add_timetable.html",
        subjects=subjects,
        faculties=faculties
    )


# 3. Edit timetable entry
@timetable.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_timetable(id):
    admin_required()

    entry = Timetable.query.get_or_404(id)
    subjects = Subject.query.all()
    faculties = Faculty.query.all()

    if request.method == "POST":
        semester = request.form.get("semester")
        section = request.form.get("section")
        subject_id = request.form.get("subject_id")
        faculty_id = request.form.get("faculty_id")
        day = request.form.get("day")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")

        if not all([
            semester, section, subject_id, faculty_id,
            day, start_time, end_time
        ]):
            flash("Please fill all required fields.", "danger")
            return redirect(url_for("timetable.edit_timetable", id=id))

        if start_time >= end_time:
            flash("End time must be later than start time.", "danger")
            return redirect(url_for("timetable.edit_timetable", id=id))

        entry.semester = int(semester)
        entry.section = section
        entry.subject_id = int(subject_id)
        entry.faculty_id = int(faculty_id)
        entry.day = day
        entry.start_time = start_time
        entry.end_time = end_time
        entry.room = request.form.get("room")

        db.session.commit()

        flash("Timetable updated successfully!", "success")
        return redirect(url_for("timetable.view_timetable"))

    return render_template(
        "admin/edit_timetable.html",
        entry=entry,
        subjects=subjects,
        faculties=faculties
    )


# 4. Delete timetable entry
@timetable.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_timetable(id):
    admin_required()

    entry = Timetable.query.get_or_404(id)

    db.session.delete(entry)
    db.session.commit()

    flash("Timetable entry deleted successfully!", "success")
    return redirect(url_for("timetable.view_timetable"))
