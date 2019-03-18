"""MCI Datastore Unit Tests

A collection of unit tests for the MCI database module.

"""

import pytest
from datetime import datetime
from expects import expect, be, equal


class TestMCIDataStore(object):
    """MCI database unit tests."""

    def test_create_new_subject(self, database):
        """Test the creation of a new MCI subject."""

        subject = Subject(
            pairin_id=123456,
            ssn=123456789,
            registration_date=datetime.now(),
            first_name='Jane',
            last_name='Doe',
            middle_name='Paulina',
            mailing_address_id=1
        )
