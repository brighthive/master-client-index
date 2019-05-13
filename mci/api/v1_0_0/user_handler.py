"""User Handler

Handle user endpoint requests from the API.

"""

import json
import os
from collections import OrderedDict
from datetime import datetime

import requests
from sqlalchemy import func

from mci.app.app import db
from mci.config import ConfigurationFactory
from mci.db.models import (Address, Disposition, EducationLevel,
                           EmploymentStatus, EthnicityRace, Gender, Individual,
                           IndividualDisposition, Source)
from mci.helpers import build_links, error_message, validate_email
from mci.id_factory import MasterClientIDFactory

config = ConfigurationFactory.from_env()


class UserHandler(object):
    """User Handler

    A class for handling all requests made to the users endpoint.

    """

    def get_mailing_address(self, user: Individual):
        """ Return an individuals mailing address if available.

        Args:
            user (Individual): The user to find the mailing address of.

        Return:
            dict: Mailing address

        """
        mailing_address = {
            'address': '',
            'city': '',
            'state': '',
            'postal_code': '',
            'country': ''
        }

        if user.mailing_address_id is not None:
            address = Address.query.filter_by(
                id=user.mailing_address_id).first()
            if address is not None:
                mailing_address['address'] = '' if address.address is None else address.address
                mailing_address['city'] = '' if address.city is None else address.city
                mailing_address['state'] = '' if address.state is None else address.state
                mailing_address['postal_code'] = '' if address.postal_code is None else address.postal_code
                mailing_address['country'] = '' if address.country is None else address.country

        return mailing_address

    def get_user_by_id(self, mci_id: str):
        """Look up a user by their MCI ID.

        Args:
            mci_id (str): The MCI ID to query for.

        Return:
            dict, int: An object representing the specified user and the associated error code.

        """

        try:
            user_obj = Individual.query.filter_by(mci_id=mci_id).first()
            if user_obj is None:
                raise Exception
            else:
                user = {
                    'mci_id': user_obj.mci_id,
                    'vendor_id': '' if user_obj.vendor_id is None else user_obj.vendor_id,
                    'registration_date': '' if user_obj.registration_date is None else datetime.strftime(user_obj.registration_date, '%Y-%m-%d'),
                    # 'ssn': '' if user_obj.ssn is None else user_obj.ssn,
                    'first_name': '' if user_obj.first_name is None else user_obj.first_name,
                    'last_name': '' if user_obj.last_name is None else user_obj.last_name,
                    'middle_name': '' if user_obj.middle_name is None else user_obj.middle_name,
                    'mailing_address': self.get_mailing_address(user_obj),
                    'date_of_birth': '' if user_obj.date_of_birth is None else str(user_obj.date_of_birth),
                    'email_address': '' if user_obj.email_address is None else user_obj.email_address,
                    'telephone': '' if user_obj.telephone is None else user_obj.telephone,
                    'gender': self.find_gender_type(user_obj),
                    'ethnicity_race': self.find_user_ethnicity(user_obj),
                    'education_level': '',
                    'employment_status': self.find_employment_status_type(user_obj),
                    'source': self.find_source_type(user_obj)
                }
                return user, 200
        except Exception as e:
            print('Exception is {}'.format(e))
            return {'error': 'Cannot find user with MCI ID {}'.format(mci_id)}, 404

    def find_address_id(self, address):
        """Look up address.

        Args:
            address (dict): The address object to query for.

        Return:
            dict: Response object with details about the address.



        """
        result = {
            'exists': False,
            'id': None,
            'error': None
        }
        try:
            new_address = Address(address['address'].title(),
                                  address['city'].title(),
                                  address['state'].upper(),
                                  address['postal_code'],
                                  address['country'].upper())
            address = Address.query.filter_by(address=new_address.address, city=new_address.city,
                                              state=new_address.state, postal_code=new_address.postal_code,
                                              country=new_address.country).first()
            if address is not None:
                result['id'] = address.id
                result['exists'] = True
            else:
                db.session.add(new_address)
                db.session.commit()
                result['id'] = new_address.id
        except Exception:
            result['error'] = 'Invalid Mailing Address format.'

        return result

    def find_gender_id(self, gender_type: str):
        """Locate Gender ID based on it's value.

        Args:
            gender_type: Gender type value to look up.

        Return:
            dict: The gender id and any associated error message.
        """
        result = {
            'id': None,
            'error': None
        }
        gender = Gender.query.filter(func.lower(
            Gender.gender) == func.lower(gender_type)).first()
        if gender is None:
            result['error'] = 'Invalid gender type specified.'
        else:
            result['id'] = gender.id

        return result

    def find_employment_status_type(self, user: Individual):
        """
        """
        try:
            employment_status = EmploymentStatus.query.filter_by(
                id=user.employment_status_id).first()
            return employment_status.employment_status
        except Exception:
            return ''

    def find_gender_type(self, user: Individual):
        """Locate Gender value based on its type.

        Args:
            gender_id: Gender type value to look up.

        Return:
            str: The gender type based on the string.
        """
        try:
            gender = Gender.query.filter_by(id=user.gender_id).first()
            return gender.gender
        except Exception:
            return ''

    def find_source_type(self, user: Individual):
        """Locate Registration source value based on its id.

        Args:
            user (Individual): Gender type value to look up.

        Return:
            str: The source type string.
        """
        try:
            source = Source.query.filter_by(id=user.source_id).first()
            return source.source
        except Exception:
            return ''

    def find_user_ethnicity(self, user: Individual):
        """Retrieve a user's ethnicities based on their IDs


        """
        ethnicities = []
        try:
            for ethnicity in user.ethnicity_races:
                ethnicities.append(ethnicity.ethnicity_race)
        except Exception:
            pass
        return ethnicities

    def find_ethnicity_race(self, ethnicity_type: str):
        """Locate Ethnicity/Race ID based on it's value.

        Args:
            ethnicity_type: Ethnicity value to look up.

        Return:
            dict: The associated ethnicity type id and any associated error message.
        """

        result = {
            'object': None,
            'error': None
        }
        try:
            ethnicity = EthnicityRace.query.filter(func.lower(
                EthnicityRace.ethnicity_race) == func.lower(ethnicity_type)).first()

            if ethnicity is not None:
                result['object'] = ethnicity
            else:
                result['error'] = 'Invalid or unknown ethnicity/race specified ({}).'.format(
                    ethnicity_type.title())
        except Exception:
            result['error'] = 'An undefined query error occured.'

        return result

    def find_education_level_id(self, education_level):
        """Locate Education Level Type ID based on it's value.

        Args:
            education_type: Education Level Type ID type value to look up.

        Return:
            dict: The education level type id and any associated error message.
        """

        result = {
            'id': None,
            'error': None
        }
        education = EducationLevel.query.filter(func.lower(
            EducationLevel.education_level) == func.lower(education_level)).first()
        if education is None:
            result['error'] = 'Invalid education level specified.'
        else:
            result['id'] = education.id

        return result

    def find_employment_status_id(self, employment_status_type):
        """Locate Employment Status Type ID based on it's value.

        Args:
            employment_status_type: Employment status type value to look up.

        Return:
            dict: The employment status type and any associated error message.
        """

        result = {
            'id': None,
            'error': None
        }
        employment_status = EmploymentStatus.query.filter(func.lower(
            EmploymentStatus.employment_status) == func.lower(employment_status_type)).first()
        if employment_status is None:
            result['error'] = 'Invalid employment status type specified.'
        else:
            result['id'] = employment_status.id

        return result

    def find_source_id(self, source_type):
        """Locate Source ID based on it's value.

        Args:
            source_type: Source type value to look up.

        Return:
            dict: The source type and any associated error message.
        """

        result = {
            'id': None,
            'error': None
        }
        source = Source.query.filter(func.lower(
            Source.source) == func.lower(source_type)).first()
        if source is None:
            result['error'] = 'Invalid source type specified.'
        else:
            result['id'] = source.id

        return result

    def find_disposition(self, disposition_type):
        """Locate Disposition based on it's value.

        Args:
            disposition_type: Disposition type value to look up.

        Return:
            dict: The associated disposition type id and any associated error message.
        """

        result = {
            'object': None,
            'error': None
        }
        try:
            disposition = Disposition.query.filter(func.lower(
                Disposition.disposition) == func.lower(disposition_type)).first()

            if disposition is not None:
                result['object'] = disposition
            else:
                result['error'] = 'Invalid or unknown disposition specified ({}).'.format(
                    disposition_type.title())
        except Exception:
            result['error'] = 'An undefined query error occured.'

        return result

    # def compute_score(self, weights: dict):
    #     score = 0.0
    #     for weight in weights.keys():
    #         score += weights[weight]
    #     return score

    # def compute_mci_threshold(self, user: Individual):
    #     """Compute the MCI Threshold for a given individual.

    #     Notes:
    #         For the purpose of this exercise, we estimate our probability to be:
    #             first_name * last_name * email_address * address * dob * ssn

    #     """
    #     match = None
    #     matched = False
    #     score = 0.0

    #     weights = {
    #         'first_name': 0.1,
    #         'last_name': 0.1,
    #         'mailing_address_id': 0.2,
    #         'date_of_birth': 0.2,
    #         'ssn': 0.4
    #     }

    #     filters = {
    #         'first_name': user.first_name,
    #         'last_name': user.last_name,
    #         'mailing_address_id': user.mailing_address_id,
    #         'date_of_birth': user.date_of_birth,
    #         'ssn': user.ssn
    #     }

    #     while not matched and len(filters.keys()) > 0:
    #         match = Individual.query.filter_by(**filters).first()
    #         if match:
    #             matched = True
    #             score = self.compute_score(weights)
    #         else:
    #             for key in weights.keys():
    #                 del(weights[key])
    #                 del(filters[key])
    #                 break
    #     return match, score

    def create_new_user(self, user_object):
        """ Creates a new user. """
        errors = []
        try:
            user = user_object.json
        except Exception:
            return error_message('Malformed or empty JSON object found in request body.')

        new_user = Individual()
        # basic user information
        if 'vendor_id' in user.keys():
            new_user.vendor_id = user['vendor_id']
        if 'ssn' in user.keys():
            new_user.ssn = user['ssn']
        if 'first_name' in user.keys():
            new_user.first_name = user['first_name'].title()
        if 'middle_name' in user.keys():
            new_user.middle_name = user['middle_name'].title()
        if 'last_name' in user.keys():
            new_user.last_name = user['last_name'].title()
        if 'email_address' in user.keys():
            if validate_email(user['email_address']):
                new_user.email_address = user['email_address']
            else:
                errors.append('Invalid Email Address format.')
        if 'telephone' in user.keys():
            new_user.telephone = user['telephone']
        if 'date_of_birth' in user.keys():
            try:
                new_user.date_of_birth = datetime.strptime(
                    user['date_of_birth'], '%Y-%m-%d')
            except Exception:
                errors.append('Invalid Date of Birth format.')

        # items that require lookup table queries
        if 'mailing_address' in user.keys():
            address = self.find_address_id(user['mailing_address'])

            if address['id'] is not None:
                new_user.mailing_address_id = address['id']
            else:
                if address['error'] is not None:
                    errors.append(address['error'])
                else:
                    errors.append('Invalid Mailing Address format.')

        if 'gender' in user.keys():
            gender = self.find_gender_id(user['gender'])
            if gender['id'] is not None:
                new_user.gender_id = gender['id']
            else:
                errors.append(gender['error'])

        if 'ethnicity_race' in user.keys():
            if not isinstance(user['ethnicity_race'], list):
                errors.append('Ethnicity/Race must be an array.')
            else:
                for ethnicities_type in user['ethnicity_race']:
                    ethnicity = self.find_ethnicity_race(ethnicities_type)
                    if ethnicity['object'] is None:
                        errors.append(ethnicity['error'])
                    else:
                        new_user.ethnicity_races.append(ethnicity['object'])

        if 'education_level' in user.keys():
            education_level = self.find_education_level_id(
                user['education_level'])
            if education_level['id'] is None:
                errors.append(education_level['error'])
            else:
                new_user.education_level_id = education_level['id']

        if 'employment_status' in user.keys():
            employment_status = self.find_employment_status_id(
                user['employment_status'])
            if employment_status['id'] is None:
                errors.append(employment_status['error'])
            else:
                new_user.employment_status_id = employment_status['id']

        if 'source' in user.keys():
            source = self.find_source_id(user['source'])
            if source['id'] is None:
                errors.append(source['error'])
            else:
                new_user.source_id = source['id']

        if 'disposition' in user.keys():
            if not isinstance(user['disposition'], list):
                errors.append('User disposition must be an array.')
            else:
                for disposition_type in user['disposition']:
                    disposition = self.find_disposition(disposition_type)
                    if disposition['object'] is None:
                        errors.append(disposition['error'])
                    else:
                        new_user.dispositions.append(disposition['object'])

        if len(errors) == 0:
            mci_threshold = os.getenv('MCI_THRESHOLD', 0.9)
            matching_service_uri = config.get_matching_service_uri()

            '''
            Should we pass the `user` json to `compute-matching` endpoint, and do the 
            normalization there? Maybe not, since: (1) the matching service would need
            to query other tables in the database, and (2) the MCI may need to create a new_user.

            Soooooo....serialize the `new_user` object.
            Question! How can we handle the date_of_birth, so that 1966-01-01 matches with 1966-1-1? 
            '''
            new_user_json = json.dumps(new_user.as_dict, default=str)

            import pdb
            pdb.set_trace()

            # How do I connect with the matching service?
            # Should I containerize the matching service, then bind it to a particular port/host?
            response = requests.post(matching_service_uri, data=new_user_json, timeout=5)

            computed_mci_threshold = response['score']
            matched_mci_id = response['mci_id']

            if computed_mci_threshold >= mci_threshold:
                matched_individual = Individual.query.filter_by(mci_id=matched_mci_id).first()
                
                return {
                    'mci_id': matched_individual.mci_id,
                    'vendor_id': matched_individual.vendor_id,
                    'first_name': matched_individual.first_name,
                    'last_name': matched_individual.last_name,
                    'match_probability': computed_mci_threshold
                }, 200
            else:
                db.session.add(new_user)
                db.session.commit()

                return {
                    'mci_id': new_user.mci_id,
                    'vendor_id': new_user.vendor_id,
                    'first_name': new_user.first_name,
                    'last_name': new_user.last_name
                }, 201
        else:
            return {
                'error': errors
            }, 400

    def get_all_users(self, offset=0, limit=20):
        """ Retrieve all users.

        Args:
            offset (int): Database offset to look up datasets by
            limit (int): Number of results to return in the query set.

        """

        status_code = 200
        try:
            offset = int(offset)
            limit = int(limit)
            if offset < 0 or limit < 0:
                return error_message('Offset and Limit must be positive integers.')
            if limit > 100:
                limit = 100
        except Exception:
            return error_message('Offset and Limit must be integers.')

        users = Individual.query.limit(limit).offset(offset)
        row_count = Individual.query.count()
        if row_count > 0:
            links = build_links('users', offset, limit, row_count)
        else:
            links = []
            status_code = 404

        response = OrderedDict()
        response['users'] = []

        for user in users:
            response['users'].append({
                'mci_id': user.mci_id,
                'first_name': user.first_name,
                'last_name': user.last_name
            })

        response['links'] = links
        return response, status_code
