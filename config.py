
import os

class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "development-only-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:YOUR_ENCODED_PASSWORD@localhost:3306/departmental_erp"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
