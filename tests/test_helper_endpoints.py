import pytest
from expects import be, be_above, expect, have_keys

from mci import app


class TestMCIAPI(object):
    def test_health_check_endpoint(self, mocker, database, test_client):
        mocker.patch(
            'brighthive_authlib.providers.AuthZeroProvider.validate_token', return_value=True)
        headers = {'Authorization': 'Bearer 1qaz2wsx3edc'}
        response = test_client.get('/health', headers=headers)
        expect(response.status_code).to(be(200))
        expect(response.json).to(
            have_keys('api_name', 'current_time', 'current_api_version', 'api_status'))
