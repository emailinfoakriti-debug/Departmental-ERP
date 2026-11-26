
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.student import Student
from models.user import User

students = Blueprint("students", __name__, url_prefix="/admin/students")


# Check admin access
def admin_required():
    return current_user.is_authenticated and current_user.role == "admin"


# View all students
@students.route("/")
@login_required
def view_students():

    if not admin_required():
        return "Access Denied!", 403

    all_students = Student.query.order_by(Student.id.desc()).all()

    return render_template(
        "admin/students.html",
        students=all_students
    )


# Add student

# Add student and create login account
@students.route("/add", methods=["GET", "POST"])
@login_required
def add_student():

    if not admin_required():
        return "Access Denied!", 403

    if request.method == "POST":

        student_id = request.form.get("student_id", "").strip()
        roll_no = request.form.get("roll_no", "").strip()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        course = request.form.get("course", "").strip()
        semester = request.form.get("semester") or None
        section = request.form.get("section", "").strip()
        password = request.form.get("password", "")

        if not all([student_id, roll_no, name, email, password]):
            flash("Please fill all required fields.")
            return redirect(url_for("students.add_student"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.")
            return redirect(url_for("students.add_student"))

        existing_student = Student.query.filter(
            (Student.student_id == student_id) |
            (Student.roll_no == roll_no) |
            (Student.email == email)
        ).first()

        if existing_student:
            flash("Student ID, roll number or email already exists.")
            return redirect(url_for("students.add_student"))

        existing_user = User.query.filter(
            (User.username == student_id) |
            (User.email == email)
        ).first()

        if existing_user:
            flash("A login account with this username or email already exists.")
            return redirect(url_for("students.add_student"))

        try:
            student = Student(
                student_id=student_id,
                roll_no=roll_no,
                name=name,
                email=email,
                phone=phone,
                course=course,
                semester=semester,
                section=section
            )

            user = User(
                username=student_id,
                email=email,
                role="student",
                status="Active"
            )

            user.set_password(password)

            db.session.add(student)
            db.session.add(user)
            db.session.commit()

            flash("Student and login account created successfully!")

        except Exception:
            db.session.rollback()
            flash("Unable to create student account. Please check the details.")
            raise

        return redirect(url_for("students.view_students"))

    return render_template("admin/add_student.html")


@students.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_student(id):

    if current_user.role != "admin":
        return "Access Denied!", 403

    student = Student.query.get_or_404(id)

    if request.method == "POST":

        student.student_id = request.form.get("student_id", "").strip()
        student.roll_no = request.form.get("roll_no", "").strip()
        student.name = request.form.get("name", "").strip()
        student.email = request.form.get("email", "").strip()
        student.phone = request.form.get("phone", "").strip()
        student.course = request.form.get("course", "").strip()
        student.semester = request.form.get("semester") or None
        student.section = request.form.get("section", "").strip()

        if not all([
            student.student_id,
            student.roll_no,
            student.name,
            student.email
        ]):
            flash("Please fill all required fields.")
            return redirect(url_for("students.edit_student", id=id))

        duplicate = Student.query.filter(
            Student.id != id,
            (
                (Student.student_id == student.student_id) |
                (Student.roll_no == student.roll_no) |
                (Student.email == student.email)
            )
        ).first()

        if duplicate:
            flash("Student ID, roll number or email already exists.")
            return redirect(url_for("students.edit_student", id=id))

        db.session.commit()

        flash("Student updated successfully!")
        return redirect(url_for("students.view_students"))

    return render_template(
        "admin/edit_student.html",
        student=student
    )

@students.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_student(id):

    if current_user.role != "admin":
        return "Access Denied!", 403

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully!")

    return redirect(url_for("students.view_students"))
