import json

import pytest

import mock
from mci_database.db.models import (Address, EducationLevel, EmploymentStatus,
                                    Individual)

from .utils import post_new_individual


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
        post_new_individual(individual_data, test_client, json_headers)

        # Confirm that the address was added to the database
        with app_configured.app_context():
            address_added_to_db = database.session.query(Address).filter_by(**address).first()
        
        assert address_added_to_db.address == address['address']
        assert address_added_to_db.city == address['city']
        assert address_added_to_db.country == address['country']

    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_find_gender_id(self, mocker, database, individual_data, gender_obj, test_client, json_headers, app_configured):
        individual_data['gender'] = 'Female'
        post_new_individual(individual_data, test_client, json_headers)

        # Confirm that the Individual with gender id was added to the database
        with app_configured.app_context():
            individual_added_to_db = database.session.query(Individual).filter(Individual.gender_id.isnot(None)).first()
        
        assert individual_added_to_db.first_name == individual_data['first_name']
        assert individual_added_to_db.last_name == individual_data['last_name']

    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_find_ethnicity_race(self, mocker, database, individual_data, ethnicity_obj, test_client, json_headers, app_configured):
        individual_data['ethnicity_race'] = ['Alaska Native']
        ind_json = post_new_individual(individual_data, test_client, json_headers)

        # Confirm that the Individual with ethnicity was added to the database by
        # querying the `individual_ethnicity_race` table.
        # Why raw sql? The `mci-database` package does not export the IndividualEthnicity model.
        with app_configured.app_context():
            query = '''
                SELECT * FROM individual_ethnicity_race 
                WHERE individual_id='{}'
            '''.format(ind_json['mci_id'])

            assert database.engine.execute(query)

    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_find_education_level(self, mocker, database, individual_data, education_obj, test_client, json_headers, app_configured):
        individual_data['education_level'] = 'Masters'
        ind_json = post_new_individual(individual_data, test_client, json_headers)

        # Confirm that the Individual with education level was added to the database
        with app_configured.app_context():
            ind_with_education = Individual.query\
                                            .join(EducationLevel)\
                                            .filter(Individual.mci_id==ind_json['mci_id'], EducationLevel.education_level=='Masters')\
                                            .first()
            
            assert ind_with_education
            assert ind_with_education.first_name == individual_data['first_name']
            assert ind_with_education.last_name == individual_data['last_name']
    
    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_find_employment_status(self, mocker, database, individual_data, employment_obj, test_client, json_headers, app_configured):
        individual_data['employment_status'] = 'Employed'
        ind_json = post_new_individual(individual_data, test_client, json_headers)

        # Confirm that the Individual with education level was added to the database
        with app_configured.app_context():
            ind_with_employment = Individual.query\
                                            .join(EmploymentStatus)\
                                            .filter(Individual.mci_id==ind_json['mci_id'], EmploymentStatus.employment_status=='Employed')\
                                            .first()
            
            assert ind_with_employment
            assert ind_with_employment.first_name == individual_data['first_name']
            assert ind_with_employment.last_name == individual_data['last_name']

    @mock.patch('brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
    def test_find_disposition(self, mocker, database, individual_data, disposition_obj, test_client, json_headers, app_configured):
        individual_data['disposition'] = ['student']
        ind_json = post_new_individual(individual_data, test_client, json_headers)

        # Confirm that the Individual with disposition was added to the database by
        # querying the `individual_disposition` table.
        # Why raw sql? The `mci-database` package does not export the IndividualDisposition model.
        with app_configured.app_context():
            query = '''
                SELECT * FROM individual_disposition 
                WHERE individual_id='{}'
            '''.format(ind_json['mci_id'])

            assert database.engine.execute(query)
