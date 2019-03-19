"""MCI ID Factory Unit Tests

A collection of unit tests for the MCI ID module.

"""

from expects import expect, be, equal
from mci.id_factory import MasterClientIDFactory


class TestIDFactory(object):
    def test_create_unique_mci_id(self, database):
        print(database)
        id1 = MasterClientIDFactory.get_id()
        id2 = MasterClientIDFactory.get_id()
        expect(id1).to_not(equal(id2))
