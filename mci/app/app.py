"""Core Appliction.

This module houses the core Flask application.

"""

from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
