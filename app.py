
from flask import Flask, render_template
from flask_login import LoginManager
from sqlalchemy import URL

from models import db

# Import database models
from models.user import User
from models.student import Student
from models.faculty import Faculty
from models.subject import Subject
from models.attendance import Attendance
from models.marks import Marks
from models.department import Department
from models.assignment import Assignment
from models.notice import Notice
from models.timetable import Timetable


# Import routes
from routes.auth import auth
from routes.admin import admin
from routes.students import students
from routes.faculty import faculty
from routes.department import department
from routes.subjects import subjects
from routes.attendance import attendance
from routes.marks import marks
from routes.assignments import assignments
from routes.notices import notices
from routes.timetable import timetable
from routes.student_portal import student_portal
from routes.faculty_portal import faculty_portal



app = Flask(__name__)

# Application settings
app.config["SECRET_KEY"] = "departmental-erp-secret-key"

# MySQL connection
# Replace YOUR_MYSQL_PASSWORD with your actual MySQL root password.
database_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="Akriti",
    host="localhost",
    port=3306,
    database="departmental_erp"
)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Connect SQLAlchemy
db.init_app(app)


# Configure Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(students)
app.register_blueprint(faculty)
app.register_blueprint(department)
app.register_blueprint(subjects)
app.register_blueprint(attendance)
app.register_blueprint(marks)
app.register_blueprint(assignments)
app.register_blueprint(notices)
app.register_blueprint(timetable)
app.register_blueprint(student_portal)
app.register_blueprint(faculty_portal)


# Home Page
@app.route("/")
def home():
    return render_template("home.html")


# Create database tables
with app.app_context():
    db.create_all()


# Run application
if __name__ == "__main__":
    app.run(debug=True)
