""" 
Whole configuration of the application.
"""

from os import environ, path
from dotenv import load_dotenv


# Base directory variable
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    """
    Enviroment variables of the application.
    """
    
    # General config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    
    
    # Firebase config
    API_KEY = environ.get('API_KEY')
    AUTH_DOMAIN = environ.get('AUTH_DOMAIN')
    DATABASE_URL = environ.get('DATABASE_URL')
    STORAGE_BUCKET = environ.get('STORAGE_BUCKET')
    GOOGLE_AUTH_APP = environ.get('GOOGLE_AUTH_APP')

    """
    # Static Assets
    STATIC_FOLDER = environ.get('STATIC_FOLDER')
    TEMPLATES_FOLDER = environ.get('TEMPLATES_FOLDER')

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    """