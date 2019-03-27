"""User Handler

Handle user endpoint requests from the API.

"""

from collections import OrderedDict
from datetime import datetime
from sqlalchemy import func
from mci.id_factory import MasterClientIDFactory
from mci.db.models import Individual, Address, EducationLevel, EmploymentStatus, EthnicityRace,\
    Gender, Source, IndividualDisposition, Disposition
from mci.app.app import db
from mci.helpers import build_links, validate_email, error_message


class UserHandler(object):
    """User Handler

    """

    def create_new_user(self, user_object):
        """ Creates a new user. """
        errors = []
        potential_match_criteria = {
            'first_name': False,
            'last_name': False,
            'email_address': False,
            'address': False,
            'date_of_birth': False,
            'ssn': False
        }

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
                return error_message('Invalid Email Address format.')
        if 'telephone' in user.keys():
            new_user.telephone = user['telephone']
        if 'date_of_birth' in user.keys():
            try:
                new_user.date_of_birth = datetime.strptime(
                    user['date_of_birth'], '%Y-%m-%d')
            except Exception:
                return error_message('Invalid Date of Birth format.')

        # items that require lookup table queries
        if 'mailing_address' in user.keys():
            provided_address = user['mailing_address']
            try:
                new_address = Address(provided_address['address'].title(),
                                      provided_address['city'].title(),
                                      provided_address['state'].upper(),
                                      provided_address['postal_code'],
                                      provided_address['country'].upper())
                address = Address.query.filter_by(address=new_address.address, city=new_address.city,
                                                  state=new_address.state, postal_code=new_address.postal_code,
                                                  country=new_address.country).first()
                if address is not None:
                    address_id = address.id
                    new_user.mailing_address_id = address.id
                    potential_match_criteria['address'] = True
                else:
                    db.session.add(new_address)
                    db.session.commit()
                    new_user.mailing_address_id = new_address.id
            except Exception:
                return error_message('Invalid Mailing Address format.')

        if 'gender' in user.keys():
            gender = Gender.query.filter(func.lower(
                Gender.gender) == func.lower(user['gender'])).first()
            if gender is None:
                return error_message('Invalid gender type specified.')
            else:
                new_user.gender_id = gender.id

        if 'ethnicity_race' in user.keys():
            if not isinstance(user['ethnicity_race'], list):
                return error_message('Ethnicity/Race must be an array.')

            for ethnicities_type in user['ethnicity_race']:
                ethnicity = EthnicityRace.query.filter(func.lower(
                    EthnicityRace.ethnicity_race) == func.lower(ethnicities_type)).first()
                if ethnicity is None:
                    return error_message('Invalid ethnicity/race type specifed.')
                else:
                    new_user.ethnicity_races.append(ethnicity)

        if 'education_level' in user.keys():
            education_level = EducationLevel.query.filter(func.lower(
                EducationLevel.education_level) == func.lower(user['education_level'])).first()
            if education_level is None:
                return error_message('Invalid education level specified.')
            else:
                new_user.education_level_id = education_level.id

        if 'employment_status' in user.keys():
            employment_status = EmploymentStatus.query.filter(func.lower(
                EmploymentStatus.employment_status) == func.lower(user['employment_status'])).first()
            if employment_status is None:
                return error_message('Invalid employment status type specified.')
            else:
                new_user.employment_status_id = employment_status.id

        if 'source' in user.keys():
            source = Source.query.filter(func.lower(
                Source.source) == func.lower(user['source'])).first()
            if source is None:
                return error_message('Invalid source type specified.')
            else:
                new_user.source_id = source.id

        if 'disposition' in user.keys():
            if not isinstance(user['disposition'], list):
                return error_message('User disposition must be an array.')
            else:
                for disposition_type in user['disposition']:
                    disposition = Disposition.query.filter(func.lower(
                        Disposition.disposition) == func.lower(disposition_type)).first()
                    if disposition is None:
                        return error_message('Invalid disposition type specifed.')
                    else:
                        new_user.dispositions.append(disposition)

        db.session.add(new_user)
        db.session.commit()

        return {
            'user_id': new_user.mci_id
        }, 201

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
