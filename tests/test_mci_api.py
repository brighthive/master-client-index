"""MCI API Unit Tests

This class contains a series of unit test geared toward exercising the MCI API.

"""

import pytest
from mci import app
from expects import expect, be, be_above, have_keys


class TestMCIAPI(object):
    """MCI API Pytest Class.

    """

    def test_health_check_endpoint(self, mocker, database, test_client):
        mocker.patch(
            'brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
        headers = {'Authorization': 'Bearer 1qaz2wsx3edc'}
        response = test_client.get('/health', headers=headers)
        expect(response.status_code).to(be(200))
        expect(response.json).to(
            have_keys('api_name', 'current_time', 'current_api_version', 'api_status'))

    def test_users_endpoint(self, mocker, database, test_client):
        mocker.patch(
            'brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
        response = test_client.get('/users')
        assert response.status_code == 404
        assert response.json['users'] == []
    
        new_user = {
            'pairin_id': '1qaz2wsx3edc',
            'ssn': '999-01-1234',
            'first_name': 'honda',
            'last_name': 'accord',
            'middle_name': 'lx',
            'mailing_address': {
                'address': 'somewhere',
                'city': 'somewhere else'
            },
            'date_of_birth': '2017-01-01',
            'email_address': 'accord@honda.com',
            'telephone': '999-124-5678',
            'gender': 'Male',
            'ethnicity_race': 'Chinese',
            'education_level': 'High School',
            'employment_status': 'Employed',
            'current_status': [
                'veteran',
                'combat wounded'
            ],
            'source': 'PAIRIN'
        }
    
    def test_get_user_bad_mci_id(self, mocker, database, test_client):
        mocker.patch(
            'brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
        response = test_client.get('/users/123badid')

        assert response.status_code == 410
        assert response.json['message']
        assert response.json['message'] == 'An individual with that ID does not exist in the MCI.'

