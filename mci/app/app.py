"""Core Appliction.

This module houses the core Flask application.

"""

from flask import Flask
from flask_restful import Api
from mci.api import HealthCheckResource

app = Flask(__name__)
api = Api(app)

api.add_resource(HealthCheckResource, '/health', endpoint='healthcheck')
