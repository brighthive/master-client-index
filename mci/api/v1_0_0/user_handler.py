"""User Handler

Handle user endpoint requests from the API.

"""

from collections import OrderedDict
from datetime import datetime
from mci.id_factory import MasterClientIDFactory
from mci.db.models import Individual, Address
from mci.app.app import db
from mci.helpers import build_links, validate_email


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
        address_id = None
        gender_id = None
        ethnicity_race_id = None
        education_level_id = None

        try:
            user = user_object.json
        except Exception:
            return {
                'error': 'Malformed or empty JSON object found in request body.'
            }, 400

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
                return {'error': 'Invalid Email Address format.'}
        if 'telephone' in user.keys():
            new_user.telephone = user['telephone']
        if 'date_of_birth' in user.keys():
            try:
                new_user.date_of_birth = datetime.strptime(
                    user['date_of_birth'], '%Y-%m-%d')
            except Exception:
                return {'error': 'Invalid Date of Birth format.'}

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
                    potential_match_criteria['address'] = True
                else:
                    db.session.add(new_address)
                    db.session.commit()
                    address_id = new_address.id
            except Exception:
                return {'error': 'Invalid mailing address format.'}, 400

        if 'gender' in user.keys():
            pass

        if 'ethnicity_race' in user.keys():
            pass

        if 'education_level' in user.keys():
            pass

        if 'employment_status' in user.keys():
            pass

        if 'current_status' in user.keys():
            pass

        if 'source' in user.keys():
            pass

        new_user.mci_id = MasterClientIDFactory.get_id()
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
                return {
                    'error': 'Offset and Limit must be positive integers.'
                }, 400
            if limit > 100:
                limit = 100
        except Exception:
            return {
                'error': 'Offset and Limit must be integers.'
            }, 400

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
