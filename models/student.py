
from models import db


class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.String(50), unique=True, nullable=False
    )

    roll_no = db.Column(
        db.String(50), unique=True, nullable=False
    )

    name = db.Column(
        db.String(100), nullable=False
    )

    email = db.Column(
        db.String(150), unique=True, nullable=False
    )

    phone = db.Column(db.String(20))

    course = db.Column(db.String(100))

    semester = db.Column(db.Integer)

    section = db.Column(db.String(20))
attendance_records = db.relationship("Attendance", backref="student")