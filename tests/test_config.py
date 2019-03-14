"""MCI API Configuration Unit Test

This class contains unit tests for the API configuration factory.

"""

from mci import ConfigurationFactory
from expects import expect, be_a, equal, have_key


class TestMCIConfiguration(object):
    """Test Configuration Factory.

    """

    def test_configuration_factory(self):
        """Test API configuration factory.

        """

        config = ConfigurationFactory.get_config('TEST')
        expect(config).to(be_a(object))
        expect(config.get_api_name()).to_not(equal('Unknown'))
        expect(config.get_api_version()).to_not(equal('Unknown'))
        expect(config.get_settings()).to(have_key('API_VERSION'))
        expect(config.get_settings()).to(have_key('API_NAME'))
