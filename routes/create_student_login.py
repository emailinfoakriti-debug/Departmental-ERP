import os
import sys

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
from models import db
from models.student import Student
from models.user import User
from app import app

with app.app_context():

    student_id = input("Enter Student ID: ").strip()

    student = Student.query.filter_by(
        student_id=student_id
    ).first()

    if not student:
        print("Student not found!")
    else:
        existing_user = User.query.filter_by(
            username=student.student_id
        ).first()

        if existing_user:
            print("Login account already exists!")
        else:
            password = input("Enter new password (minimum 8 characters): ")

            if len(password) < 8:
                print("Password must contain at least 8 characters.")
            else:
                user = User(
                    username=student.student_id,
                    email=student.email,
                    role="student",
                    status="Active"
                )

                user.set_password(password)

                db.session.add(user)
                db.session.commit()

                print("Student login account created successfully!")
