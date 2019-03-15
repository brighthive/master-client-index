"""Core Appliction.

This module houses the core Flask application.

"""

from flask import Flask
from flask_restful import Api
from mci.api import HealthCheckResource, UserResource

app = Flask(__name__)
api = Api(app)

api.add_resource(HealthCheckResource, '/health', endpoint='healthcheck')
api.add_resource(UserResource, '/users', endpoint='users')
