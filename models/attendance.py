
from models import db

class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    date = db.Column(db.Date, nullable=False)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Present"
    )

    remarks = db.Column(db.String(255))
