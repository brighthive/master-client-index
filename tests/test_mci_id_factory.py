"""MCI ID Factory Unit Tests

A collection of unit tests for the MCI ID module.

"""

from expects import expect, be, equal
from mci.id_factory import IDFactory


class TestIDFactory(object):
    def test_create_unique_mci_id(self):
        id1 = IDFactory.get_id()
        id2 = IDFactory.get_id()
        expect(id1).to_not(equal(id2))
