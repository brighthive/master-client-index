"""Core Appliction.

This module houses the core Flask application.

"""

import json

from brighthive_authlib import OAuth2ProviderError
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from mci.api import (AddressResource, DispositionResource,
                     EducationLevelResource, EmploymentStatusResource,
                     EthnicityRaceResource, GenderResource,
                     HealthCheckResource, SourceResource, UserDetailResource,
                     UserResource)
from mci.config import ConfigurationFactory
from mci_database.db import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(ConfigurationFactory.from_env())
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    # core endpoints
    api.add_resource(UserResource, '/users', endpoint='users_ep')
    api.add_resource(UserDetailResource, '/users/<mci_id>',
                     endpoint='user_detail_ep')
    # helper endpoints
    api.add_resource(HealthCheckResource, '/health', endpoint='healthcheck_ep')
    api.add_resource(SourceResource, '/source', endpoint='sources_ep')
    api.add_resource(GenderResource, '/gender', endpoint='gender_ep')
    api.add_resource(AddressResource, '/address', endpoint='address_ep')
    api.add_resource(DispositionResource, '/disposition',
                     endpoint='disposition_ep')
    api.add_resource(EthnicityRaceResource, '/ethnicity',
                     endpoint='ethnicities_ep')
    api.add_resource(EmploymentStatusResource, '/employment_status',
                     endpoint='employment_status_ep')
    api.add_resource(EducationLevelResource, '/education_level',
                     endpoint='education_ep')

    @app.errorhandler(Exception)
    def handle_errors(e):
        if isinstance(e, OAuth2ProviderError):
            return json.dumps({'message': 'Access Denied'}), 401
        else:
            try:
                error_code = str(e).split(':')[0][:3].strip()
                error_text = str(e).split(':')[0][3:].strip()
                if isinstance(error_code, int):
                    return json.dumps({'error': error_text}), error_code
                else:
                    raise Exception
            except Exception as e:
                print(e)
                return json.dumps({'error': 'An unknown error occured'}), 400
    
    return app
