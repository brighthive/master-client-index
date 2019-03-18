"""Core Appliction.

This module houses the core Flask application.

"""

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from mci.config import ConfigurationFactory
from mci.api import HealthCheckResource, UserResource

app = Flask(__name__)
app.config.from_object(ConfigurationFactory.from_env())
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

api.add_resource(HealthCheckResource, '/health', endpoint='healthcheck')
api.add_resource(UserResource, '/users', endpoint='users')
