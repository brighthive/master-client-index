"""User Resource

This class represents a user registered with the Master Client Index.

"""

from flask import request
from mci.api import VersionedResource, V1_0_0_UserHandler


class UserResource(VersionedResource):
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
            request_handler = V1_0_0_UserHandler()
        else:
            request_handler = V1_0_0_UserHandler()

        return request_handler

    def get(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).get_all_users()

    def post(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).get_health()

    def put(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).get_health()

    def patch(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).get_health()

    def delete(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).get_health()
