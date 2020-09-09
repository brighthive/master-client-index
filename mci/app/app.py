"""Core Appliction.

This module houses the core Flask application.

"""

import os
import json
import logging
from brighthive_authlib import OAuth2ProviderError
from flask import Flask, jsonify, request
from datetime import datetime
from flask_migrate import Migrate
from flask_restful import Api
import boto3.session
import watchtower
from flask_sqlalchemy import SQLAlchemy

from mci.api import (AddressResource, DispositionResource,
                     EducationLevelResource, EmploymentStatusResource,
                     EthnicityRaceResource, GenderResource,
                     HealthCheckResource, SourceResource, UserDetailResource,
                     UserResource, UserRemovePIIResource)
from mci.api.errors import IndividualDoesNotExist
from mci.config import ConfigurationFactory
from mci_database.db import db

# logger configuration
formatter = logging.Formatter(
    fmt='[%(asctime)s] [%(levelname)s] %(message)s', datefmt="%a, %d %b %Y %H:%M:%S")

try:
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region_name = os.getenv('AWS_REGION_NAME')
    logging.getLogger().setLevel(logging.INFO)
    boto3_session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                                  region_name=region_name)
    logger = logging.getLogger(__name__)
    handler = watchtower.CloudWatchLogHandler(
        boto3_session=boto3_session, log_group=os.getenv('AWS_LOG_GROUP'), stream_name=os.getenv('AWS_LOG_STREAM'))
    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)s] %(message)s', datefmt="%a, %d %b %Y %H:%M:%S")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
except Exception as e:
    logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.warning(
        f'Failed to configure CloudWatch due to the following error: {str(e)}')


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
            response = jsonify({'error': 'An unknown error occured'})
            response.status_code = 400
            return response


def after_request(response):
    info = {
        'remote_addr': request.remote_addr,
        'request_time': str(datetime.utcnow()),
        'method': request.method,
        'path': request.path,
        'scheme': request.scheme.upper(),
        'status_code': response.status_code,
        'status': response.status,
        'content_length': response.content_length,
        'user_agent': str(request.user_agent)
    }
    if info['status_code'] >= 200 and info['status_code'] < 300:
        logger.info(info)
    else:
        logger.error(info)
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
    api.add_resource(HealthCheckResource, '/', endpoint='healthcheck_ep')
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
    app.after_request(after_request)
    return app
