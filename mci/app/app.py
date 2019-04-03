"""Core Appliction.

This module houses the core Flask application.

"""

import json
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from brighthive_authlib import OAuth2ProviderError
from mci.config import ConfigurationFactory

app = Flask(__name__)
app.config.from_object(ConfigurationFactory.from_env())
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

if db:
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


@app.errorhandler(Exception)
def handle_errors(e):
    if isinstance(e, OAuth2ProviderError):
        return json.dumps({'message': 'Access Denied'}), 401
    else:
        try:
            error_code = str(e).split(':')[0][:3].strip()
            error_text = str(e).split(':')[0][3:].strip()
            return json.dumps({'error': error_text}), error_code
        except Exception:
            return json.dumps({'error': 'An unknown error occured'}), 400
