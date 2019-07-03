import json

import pytest
import mock
import requests_mock

from mci import app
from mci_database import db
from mci_database.db.models import Individual
from mci.api.v1_0_0.user_handler import UserHandler

class TestUserHelpers(object):
    def test_get_mailling_address(self, database, individual, app_configured):
        new_individual = Individual(**individual)

        with app_configured.app_context():
            database.session.add(new_individual) 
            database.session.commit()
        
        UserHandler._get_mailing_address()

