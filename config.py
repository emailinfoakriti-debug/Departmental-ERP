
import os

class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "development-only-secret-key"
    )

    database_url = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:YOUR_ENCODED_PASSWORD@localhost:3306/departmental_erp"
    )

    # Convert Railway's mysql:// URL to SQLAlchemy's PyMySQL format
    if database_url.startswith("mysql://"):
        database_url = database_url.replace(
            "mysql://",
            "mysql+pymysql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = database_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False
