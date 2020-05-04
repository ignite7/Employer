""" 
Initialize the application and configuration.
"""

# Flask libraries
from flask import Flask
from flask_bootstrap import Bootstrap


# Local modules
from .config import Config
import pdb


def _create_app():
    """
    Funtion manager to create the 
    application and set the config file.
    """
    
    app = Flask(__name__) # Name app
    
    bootstrap = Bootstrap(app) # Converting in Bootstrap app

    app.config.from_object(Config) # Call the files configurations

    return app
