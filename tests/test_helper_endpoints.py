import pytest
from expects import be, be_above, expect, have_keys

from mci import app


class TestMCIAPI(object):
    def test_health_check_endpoint(self, test_client):
        headers = {'Content-Type': 'application/json'}
        response = test_client.get('/', headers=headers)
        expect(response.status_code).to(be(200))
        expect(response.json).to(
            have_keys('api_name', 'current_time', 'current_api_version', 'api_status'))
