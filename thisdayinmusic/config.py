"""Default configuration

Use env var to override
"""
import os

DEBUG = True
SECRET_KEY = "changeme"

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
