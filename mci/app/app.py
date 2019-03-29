"""Core Appliction.

This module houses the core Flask application.

"""

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from brighthive_authlib import OAuth2ProviderError
from mci.config import ConfigurationFactory


def handle_auth_denied(e):
    print('Handline access denied maybe?')
    return {'message': 'Access Denied'}, 401


app = Flask(__name__)
app.config.from_object(ConfigurationFactory.from_env())
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

if db:
    # import mci.db.models
    from mci.api import UserResource, HealthCheckResource

    # core endpoints
    api.add_resource(UserResource, '/users', endpoint='users_ep')
    api.add_resource(HealthCheckResource, '/referrals',
                     endpoint='referrals_ep')

    # from data resource api
    api.add_resource(HealthCheckResource, '/programs', endpoint='programs_ep')
    api.add_resource(HealthCheckResource, '/providers',
                     endpoint='providers_ep')

    # helper endpoints
    api.add_resource(HealthCheckResource, '/health', endpoint='healthcheck_ep')
    api.add_resource(HealthCheckResource, '/sources', endpoint='sources_ep')
    api.add_resource(HealthCheckResource, '/genders', endpoint='gender_ep')
    api.add_resource(HealthCheckResource, '/ethnicities',
                     endpoint='ethnicities_ep')
    api.add_resource(HealthCheckResource, '/education',
                     endpoint='education_ep')
    api.add_resource(HealthCheckResource, '/employment',
                     endpoint='employment_ep')
    api.add_resource(HealthCheckResource, '/status', endpoint='status_ep')


@app.errorhandler(OAuth2ProviderError)
def handle_auth_denied(e):
    print('Handline access denied maybe?')
    return {'message': 'Access Denied'}, 401
