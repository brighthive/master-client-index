import json

import requests_mock


def post_new_individual(individual_data, test_client, headers):
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
