"""MCI Datastore Unit Tests

A collection of unit tests for the MCI database module.

"""

import pytest
from expects import expect, be, equal


class TestMCIDataStore(object):
    def test_foo(self):
        expect("foo").to(equal("foo"))
