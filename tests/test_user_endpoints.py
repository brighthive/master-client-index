import json

import pytest
import mock
import requests_mock
from expects import be, be_above, expect, have_keys

from mci import app
from mci_database import db
from mci_database.db.models import Individual

from .utils import post_new_individual

class TestMCIAPI(object):
    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_users_endpoint_empty(self, mocker, database, test_client):
        '''
        Tests that the users endpoint returns expected content when the database is empty.
        '''
        response = test_client.get('/users')

        assert response.status_code == 404
        assert response.json['users'] == []
    
    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_users_endpoint_populated(self, mocker, database, individual_data, test_client, json_headers):
        '''
        Tests that the users endpoint returns expected content when the database has Individual entries.
        '''
        post_new_individual(individual_data, test_client, json_headers)

        response = test_client.get('/users')

        assert response.status_code == 200
        assert isinstance(response.json['users'][0], dict)
        assert 'mci_id' in response.json['users'][0].keys()

    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_get_user_invalid(self, mocker, database, test_client):
        '''
        Tests that GETing an invalid user returns the correct error message.
        '''
        response = test_client.get('/users/123badid')

        assert response.status_code == 410
        assert response.json['message']
        assert response.json['message'] == 'An individual with that ID does not exist in the MCI.'
    
    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_get_user_valid(self, mocker, database, individual_data, test_client, json_headers):
        '''
        Tests that GETing a valid user returns the JSON and 200 status code.
        '''
        new_individual = post_new_individual(individual_data, test_client, json_headers)

        response = test_client.get('/users/{}'.format(new_individual['mci_id']))

        assert response.status_code == 200
        assert response.json
    
    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_post_users_existing(self, mocker, database, individual_data, test_client, json_headers):
        '''
        Tests that POSTing an existing user returns a 200 with correct user information.
        '''        
        new_individual = post_new_individual(individual_data, test_client, json_headers)

        with requests_mock.Mocker() as m:
            m.post("http://mcimatchingservice_mci_1:8000/compute-match",
                  json={"mci_id": new_individual['mci_id'], "score": 10.0}, status_code=201)

            response = test_client.post('/users', data=json.dumps(individual_data), headers=json_headers)

        assert response.status_code == 200
        assert response.json['first_name'] == individual_data['first_name']
        assert response.json['last_name'] == individual_data['last_name']
        assert response.json['mci_id'] == new_individual['mci_id']
        assert response.json['match_probability'] == 10.0

    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_post_users_bad_json(self, mocker, test_client, json_headers):
        with requests_mock.Mocker() as m:
            m.post("http://mcimatchingservice_mci_1:8000/compute-match",
                  json={"mci_id": "", "score": ""}, status_code=201)

            bad_json = {
                'first_name': "Single",
                'middle_name': "Quote",
                'last_name': "Mistake",
            }

            response = test_client.post('/users', data=bad_json, headers=json_headers)
            assert response.status_code == 400
            assert response.json['error'] == 'Malformed or empty JSON object found in request body.'

    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_post_users_matching_down(self, mocker, individual_data, test_client, json_headers):
        response = test_client.post('/users', data=json.dumps(individual_data), headers=json_headers)

        assert response.status_code == 400
        assert response.json['error'] == 'The matching service did not return a response.'

    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_remove_pii_invalid_id(self, mocker, database, test_client, json_headers):
        response = test_client.post(
            '/users/remove-pii', data=json.dumps({"mci_id": "123fakeid"}), headers=json_headers)
        
        assert response.status_code == 410
        assert response.json['message'] == 'An individual with that ID does not exist in the MCI.'
    
    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_remove_pii_valid_id(self, mocker, app_configured, database, individual_data, test_client, json_headers):
        new_individual = post_new_individual(individual_data, test_client, json_headers)
        
        with app_configured.app_context():
            assert database.session.query(Individual).filter_by(first_name=individual_data['first_name']).first()

            response = test_client.post(
                '/users/remove-pii',
                data=json.dumps({"mci_id": new_individual['mci_id']}),
                headers=json_headers)

            assert response.status_code == 201

            updated_individual = database.session.query(Individual).filter_by(mci_id=new_individual['mci_id']).first()
            assert updated_individual.first_name == None
            assert updated_individual.last_name == None
            assert updated_individual.middle_name == None
            assert updated_individual.date_of_birth == None
            assert updated_individual.email_address == None
            assert updated_individual.telephone == None
            assert updated_individual.ssn == None
