"""MCI Datastore Unit Tests

A collection of unit tests for the MCI database module.

"""

import pytest
from datetime import datetime
from expects import expect, be, equal
from mci.db.models import Gender, Individual


class TestMCIDataStore(object):
    """MCI database unit tests."""

    def test_database_operations(self, database):
        # add datasets to datastore
        pass
