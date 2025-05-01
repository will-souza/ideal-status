import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_secret_key')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    DB_NAME = ''
    DB_USERNAME = ''
    DB_PASSWORD = ''

    IMAGE_UPLOADS = ''

    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    DB_NAME = ''
    DB_USERNAME = ''
    DB_PASSWORD = ''

    IMAGE_UPLOADS = ''

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///testing.sqlite3')
    DB_NAME = ''
    DB_USERNAME = ''
    DB_PASSWORD = ''

    SESSION_COOKIE_SECURE = False