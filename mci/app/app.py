"""Core Appliction.

This module houses the core Flask application.

"""

import json

from brighthive_authlib import OAuth2ProviderError
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from mci.api import (AddressResource, DispositionResource,
                     EducationLevelResource, EmploymentStatusResource,
                     EthnicityRaceResource, GenderResource,
                     HealthCheckResource, SourceResource, UserDetailResource,
                     UserResource, UserRemovePIIResource)
from mci.api.errors import IndividualDoesNotExist
from mci.config import ConfigurationFactory
from mci_database.db import db

def handle_errors(e):
    if isinstance(e, OAuth2ProviderError):
        response = jsonify({'message': 'Access Denied'})
        response.status_code = 401
        return response
    elif isinstance(e, IndividualDoesNotExist):
        response = jsonify(
            {'message': 'An individual with that ID does not exist in the MCI.'})
        response.status_code = 410
        return response
    else:
        try:
            error_code = str(e).split(':')[0][:3].strip()
            error_text = str(e).split(':')[0][3:].strip()
            if isinstance(error_code, int):
                response = jsonify({'error': error_text})
                response.status_code = error_code
                return response
            else:
                raise Exception
        except Exception as e:
            print(e)
            response = jsonify({'error': 'An unknown error occured'})
            response.status_code = 400
            return response


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
    api.add_resource(UserRemovePIIResource, '/users/remove-pii',
                     endpoint='user_remove_pii_ep')
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

    app.register_error_handler(Exception, handle_errors)
    return app
