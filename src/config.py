"""App config"""
import os
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

class Config:
    DEBUG = True
    TESTING = False

    CSRF_ENABLED = False

    VELO_API_ACCESSTOKEN = os.getenv("VELO_API_ACCESSTOKEN")
    VELO_API_ACCESSTOKENEXPIRATION = os.getenv("VELO_API_ACCESSTOKENEXPIRATION")
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")
