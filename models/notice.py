
from models import db


class Notice(db.Model):

    __tablename__ = "notices"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text, nullable=False)

    category = db.Column(db.String(50))

    publish_date = db.Column(db.Date, nullable=False)

    expiry_date = db.Column(db.Date)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )
