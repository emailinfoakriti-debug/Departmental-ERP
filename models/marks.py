
from models import db

class Marks(db.Model):
    __tablename__ = "marks"

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

    exam_name = db.Column(db.String(100))

    assignment_marks = db.Column(db.Float)

    internal_marks = db.Column(db.Float)

    practical_marks = db.Column(db.Float)

    total_marks = db.Column(db.Float)
