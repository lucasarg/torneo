import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    # Secret key for session/CSRF; load from .env in real setups
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-insecure-change-me")
    # SQLite DB stored in instance/ (ignored by git by default)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'instance' / 'torneo.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
