"""MCI API Unit Tests

This class contains a series of unit test geared toward exercising the MCI API.

"""

import pytest
from mci import app
from expects import expect, be, be_above


class TestMCIAPI(object):
    """MCI API Pytest Class.

    """

    @pytest.fixture
    def test_client(self):
        return app.test_client()

    def test_health_check(self, test_client):
        response = test_client.get('/health')
        expect(response.status_code).to(be(200))
