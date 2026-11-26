
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from getpass import getpass
from app import app
from models import db
from models.user import User
from models.faculty import Faculty


with app.app_context():

    faculty_id = input("Enter Faculty ID: ").strip()

    faculty = Faculty.query.filter_by(
        faculty_id=faculty_id
    ).first()

    if not faculty:
        print("Faculty record not found!")
    else:
        existing = User.query.filter(
            (User.username == faculty.faculty_id) |
            (User.email == faculty.email)
        ).first()

        if existing:
            print("A user account with this ID or email already exists.")
        else:
            password = input("Create faculty password: ")

            if len(password) < 8:
                print("Password must contain at least 8 characters.")
            else:
                user = User(
                    username=faculty.faculty_id,
                    email=faculty.email,
                    role="faculty",
                    status="Active"
                )

                user.set_password(password)

                db.session.add(user)
                db.session.commit()

                print("Faculty login account created successfully!")
