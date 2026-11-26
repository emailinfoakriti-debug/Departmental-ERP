from models import db

class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    subject_code = db.Column(db.String(50), unique=True, nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    credits = db.Column(db.Integer, default=4)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))

    # ADD THIS LINE HERE
    attendance_records = db.relationship("Attendance", backref="subject")