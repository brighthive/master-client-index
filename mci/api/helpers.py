"""Source Resource

This class represents a user registered with the Master Client Index.

"""

from flask import request
from brighthive_authlib import token_required
from mci.api import VersionedResource, V1_0_0_HelperHandler
from mci.config import Config


class HelperResource(VersionedResource):
    """Represents a user registered in the MCI.

    """

    def __init__(self):
        super().__init__()

    def get_request_handler(self, headers):
        """Retrieve request handler based on API version number.

        Args:
            headers (dict): HTTP request headers passed in by the client.

        Returns:
            object: API request handler based on version number.

        """
        api_version = self.get_api_version(headers)

        if api_version == '1.0.0':
            request_handler = V1_0_0_HelperHandler()
        else:
            request_handler = V1_0_0_HelperHandler()

        return request_handler


class SourceResource(HelperResource):
    def __init__(self):
        super().__init__()

    @token_required(Config.get_oauth2_provider())
    def get(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """

        return self.get_request_handler(request.headers).get_all_sources()

    @token_required(Config.get_oauth2_provider())
    def post(self):
        """ Handle POST request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).create_new_source(request)


class GenderResource(HelperResource):
    def __init__(self):
        super().__init__()

    @token_required(Config.get_oauth2_provider())
    def get(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """

        return self.get_request_handler(request.headers).get_all_genders()

    @token_required(Config.get_oauth2_provider())
    def post(self):
        """ Handle POST request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).create_new_gender(request)


class AddressResource(HelperResource):
    def __init__(self):
        super().__init__()

    @token_required(Config.get_oauth2_provider())
    def get(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """

        return self.get_request_handler(request.headers).get_all_addresses()

    @token_required(Config.get_oauth2_provider())
    def post(self):
        """ Handle POST request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).create_new_address(request)


class DispositionResource(HelperResource):
    def __init__(self):
        super().__init__()

    @token_required(Config.get_oauth2_provider())
    def get(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """

        return self.get_request_handler(request.headers).get_all_dispositions()

    @token_required(Config.get_oauth2_provider())
    def post(self):
        """ Handle POST request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).create_new_disposition(request)


class EducationLevelResource(HelperResource):
    def __init__(self):
        super().__init__()

    @token_required(Config.get_oauth2_provider())
    def get(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """

        return self.get_request_handler(request.headers).get_all_education_levels()

    @token_required(Config.get_oauth2_provider())
    def post(self):
        """ Handle POST request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).create_new_education_level(request)


class EmploymentStatusResource(HelperResource):
    def __init__(self):
        super().__init__()

    @token_required(Config.get_oauth2_provider())
    def get(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """

        return self.get_request_handler(request.headers).get_all_employment_status()

    @token_required(Config.get_oauth2_provider())
    def post(self):
        """ Handle POST request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).create_new_employment_status(request)


class EthnicityRaceResource(HelperResource):
    def __init__(self):
        super().__init__()

    @token_required(Config.get_oauth2_provider())
    def get(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """

        return self.get_request_handler(request.headers).get_all_ethnicities()

    @token_required(Config.get_oauth2_provider())
    def post(self):
        """ Handle POST request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).create_new_ethnicity(request)
