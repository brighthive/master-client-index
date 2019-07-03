import json

import pytest
import mock
import requests_mock

from mci import app
from mci_database import db
from mci_database.db.models import Individual, Address
from mci.api.v1_0_0.user_handler import UserHandler

class TestUserHelpers(object):
    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_get_mailling_address(self, mocker, test_client, individual_obj):
        response = test_client.get('/users/{}'.format(individual_obj))

        assert response.status_code == 200
        assert response.json['mailing_address']['address'] == '25 Brook St'
        assert response.json['mailing_address']['city'] == 'London'
    
    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_find_address_id_create(self, mocker, database, individual_data, test_client, json_headers, app_configured):
        address = {
            'address': '233 N Michigan',
            'city': 'Chicago',
            'country': 'US',
        }

        individual_data['mailing_address'] = address

        # POST a new indvidual with an address
        self._post_new_individual(individual_data, test_client, json_headers)

        # Confirm that the address was added to the database
        with app_configured.app_context():
            address_added_to_db = database.session.query(Address).filter_by(**address).first()
        
        assert address_added_to_db.address == address['address']
        assert address_added_to_db.city == address['city']
        assert address_added_to_db.country == address['country']

    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_find_gender_id(self, mocker, database, individual_data, gender_obj, test_client, json_headers, app_configured):
        individual_data['gender'] = 'Female'

        # POST a new indvidual with a gender
        self._post_new_individual(individual_data, test_client, json_headers)

        # Confirm that the Individual with gender id was added to the database
        with app_configured.app_context():
            individual_added_to_db = database.session.query(Individual).filter(Individual.gender_id.isnot(None)).first()
        
        assert individual_added_to_db.first_name == individual_data['first_name']
        assert individual_added_to_db.last_name == individual_data['last_name']

    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_find_ethnicity_race(self, mocker, database, individual_data, ethnicity_obj, test_client, json_headers, app_configured):
        individual_data['ethnicity_race'] = ['Alaska Native']

        # POST a new indvidual with an ethnicity
        ind_json = self._post_new_individual(individual_data, test_client, json_headers)

        # Confirm that the Individual with ethnicity was added to the database – by way of individual_ethnicity_race join table
        with app_configured.app_context():

            query = "SELECT * FROM individual_ethnicity_race WHERE individual_id='{}'".format(ind_json['mci_id'])
            assert database.engine.execute(query)

    def _post_new_individual(self, individual_data, test_client, headers):
        '''
        Helper function for posting a new Individual to the MCI.
        Returns the JSON for the newly created Individual.
        '''
        with requests_mock.Mocker() as m:
            m.post("http://mcimatchingservice_mci_1:8000/compute-match",
                  json={"mci_id": "", "score": ""}, status_code=201)

            response = test_client.post('/users', data=json.dumps(individual_data), headers=headers)

            assert response.status_code == 201
            assert response.json['first_name'] == individual_data['first_name']
            assert response.json['last_name'] == individual_data['last_name']
        
        return response.json
        

