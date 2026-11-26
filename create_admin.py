
from app import app
from models import db
from models.user import User

with app.app_context():

    existing_user = User.query.filter_by(
        username="admin"
    ).first()

    if existing_user:
        print("Admin account already exists.")

    else:
        admin = User(
            username="admin",
            email="admin@department.com",
            role="admin",
            status="Active"
        )

        admin.set_password(os.environ["ADMIN_PASSWORD"])

        db.session.add(admin)
        db.session.commit()

        print("Admin account created successfully!")
