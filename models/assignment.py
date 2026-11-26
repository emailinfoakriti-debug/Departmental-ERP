
from models import db


class Assignment(db.Model):

    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text)

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    faculty_name = db.Column(db.String(100))

    due_date = db.Column(db.Date, nullable=False)

    total_marks = db.Column(db.Float, default=100)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )
