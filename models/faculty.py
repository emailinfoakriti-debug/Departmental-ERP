
from models import db


class Faculty(db.Model):

    __tablename__ = "faculty"

    id = db.Column(db.Integer, primary_key=True)

    faculty_id = db.Column(
        db.String(50), unique=True, nullable=False
    )

    name = db.Column(
        db.String(100), nullable=False
    )

    email = db.Column(
        db.String(150), unique=True, nullable=False
    )

    phone = db.Column(db.String(20))

    department = db.Column(db.String(100))

    designation = db.Column(db.String(100))

    qualification = db.Column(db.String(150))
