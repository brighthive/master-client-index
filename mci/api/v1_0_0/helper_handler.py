"""User Handler

Handle user endpoint requests from the API.

"""

import os
from collections import OrderedDict
from datetime import datetime

from mci_database.db import db
from mci_database.db.models import (Address, Disposition, EducationLevel,
                                    EmploymentStatus, EthnicityRace, Gender,
                                    Individual, IndividualDisposition, Source)
from sqlalchemy import func

from mci.config import Config
from mci.helpers import build_links, error_message, validate_email


class HelperHandler(object):
    """Helper Handler

    A class for handling all minor queries.

    """

    def get_all_education_levels(self):
        """Return all education level codes."""
        try:
            response = {'education_levels': []}
            education_levels = EducationLevel.query.all()
            for education_level in education_levels:
                response['education_levels'].append({
                    'id': education_level.id,
                    'education_level': education_level.education_level
                })
            return response, 200
        except Exception as e:
            return {'error': 'Not Found {}'.format(e)}, 404

    def create_new_education_level(self, request_obj):
        """Create a new education level code."""

        try:
            education_level_obj = request_obj.json
        except Exception:
            return {'error': 'Invalid request'}, 400

        try:
            education_level = EducationLevel(
                education_level_obj['education_level'])
            db.session.add(education_level)
            db.session.commit()
            return {'success': 'New education level', 'id': education_level.id}, 201
        except Exception:
            return {'error': 'Invalid request'}, 400

    def get_all_employment_status(self):
        """Return all employment status codes."""
        try:
            response = {'employment_status': []}
            employmet_statuses = EmploymentStatus.query.all()
            for employment_status in employmet_statuses:
                response['employment_status'].append({
                    'id': employment_status.id,
                    'employment_status': employment_status.employment_status
                })
            return response, 200
        except Exception as e:
            return {'error': 'Not Found {}'.format(e)}, 404

    def create_new_employment_status(self, request_obj):
        """Create a new employment status code."""

        try:
            employment_status_obj = request_obj.json
        except Exception:
            return {'error': 'Invalid request'}, 400

        try:
            employment_status = EmploymentStatus(
                employment_status_obj['employment_status'])
            db.session.add(employment_status)
            db.session.commit()
            return {'success': 'New employment status', 'id': employment_status.id}, 201
        except Exception:
            return {'error': 'Invalid request'}, 400

    def get_all_ethnicities(self):
        """Return all ethnicity codes known to the application."""
        try:
            response = {'ethnicities': []}
            ethnicity_races = EthnicityRace.query.all()
            for ethnicity_race in ethnicity_races:
                response['ethnicities'].append({
                    'id': ethnicity_race.id,
                    'ethnicity_Race': ethnicity_race.ethnicity_race
                })
            return response, 200
        except Exception as e:
            return {'error': 'Not Found {}'.format(e)}, 404

    def create_new_ethnicity(self, request_obj):
        """Create a new ethnicity code."""

        try:
            ethnicity_obj = request_obj.json
        except Exception:
            return {'error': 'Invalid request'}, 400

        try:
            ethnicity = EthnicityRace(ethnicity_obj['ethnicity_race'])
            db.session.add(ethnicity)
            db.session.commit()
            return {'success': 'New ethnicity created', 'id': ethnicity.id}, 201
        except Exception:
            return {'error': 'Invalid request'}, 400

    def get_all_dispositions(self):
        """Return all individual disposition codes."""
        try:
            response = {'dispositions': []}
            dispositions = Disposition.query.all()
            for disposition in dispositions:
                response['dispositions'].append({
                    'id': disposition.id,
                    'disposition': disposition.disposition
                })
            return response, 200
        except Exception as e:
            return {'error': 'Not Found {}'.format(e)}, 404

    def create_new_disposition(self, request_obj):
        """Create a new disposition code."""

        try:
            disposition_obj = request_obj.json
        except Exception:
            return {'error': 'Invalid request'}, 400

        try:
            disposition = Disposition(disposition_obj['disposition'])
            db.session.add(disposition)
            db.session.commit()
            return {'success': 'New disposition created', 'id': disposition.id}, 201
        except Exception:
            return {'error': 'Invalid request'}, 400

    def get_all_addresses(self):
        """Return all addresses known to the application."""
        try:
            response = {'addresses': []}
            addresses = Address.query.all()
            for address in addresses:
                response['addresses'].append({
                    'id': address.id,
                    'address': address.address,
                    'city': address.city,
                    'postal_code': address.postal_code,
                    'country': address.country
                })
            return response, 200
        except Exception as e:
            return {'error': 'Not Found {}'.format(e)}, 404

    def create_new_address(self, request_obj):
        """Create a new address."""

        try:
            address_obj = request_obj.json
        except Exception:
            return {'error': 'Invalid request'}, 400

        try:
            address = Address(address_obj['address'], address_obj['city'],
                              address_obj['state'], address_obj['postal_code'], address_obj['country'])
            db.session.add(address)
            db.session.commit()
            return {'success': 'New address created', 'id': address.id}, 201
        except Exception:
            return {'error': 'Invalid request'}, 400

    def get_all_sources(self):
        """Return all sources known to the application."""
        try:
            response = {'sources': []}
            sources = Source.query.all()
            for source in sources:
                response['sources'].append({
                    'id': source.id,
                    'source': source.source
                })
            return response, 200
        except Exception:
            return {'error': 'Not Found {}'}, 404

    def create_new_source(self, request_obj):
        """Create a new source."""

        try:
            source_obj = request_obj.json
        except Exception:
            return {'error': 'Invalid request'}, 400

        try:
            source = Source(source_obj['source'])
            db.session.add(source)
            db.session.commit()
            return {'success': 'New source created', 'id': source.id}, 201
        except Exception:
            return {'error': 'Invalid request'}, 400

    def get_all_genders(self):
        """Return all genders known to the application."""
        try:
            response = {'genders': []}
            genders = Gender.query.all()
            for gender in genders:
                response['genders'].append({
                    'id': gender.id,
                    'gender': gender.gender
                })
            return response, 200
        except Exception:
            return {'error': 'Not Found'}, 404

    def create_new_gender(self, request_obj):
        """Create a new gender."""

        try:
            source_obj = request_obj.json
        except Exception:
            return {'error': 'Invalid request'}, 400

        try:
            gender = Gender(source_obj['gender'])
            db.session.add(gender)
            db.session.commit()
            return {'success': 'New gender created', 'id': gender.id}, 201
        except Exception:
            return {'error': 'Invalid request'}, 400
