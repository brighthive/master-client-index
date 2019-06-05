"""User Resource

This class represents a user registered with the Master Client Index.

"""

from flask import request
from brighthive_authlib import token_required
from mci.api import VersionedResource, V1_0_0_UserHandler
from mci.config import Config


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

    @token_required(Config.get_oauth2_provider())
    def get(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """

        offset = 0
        limit = 20
        args = request.args
        try:
            offset = request.args['offset']
        except Exception:
            pass

        try:
            limit = request.args['limit']
        except Exception:
            pass

        return self.get_request_handler(request.headers).get_all_users(offset=offset, limit=limit)

    @token_required(Config.get_oauth2_provider())
    def post(self):
        """ Handle POST request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).create_new_user(request)

    @token_required(Config.get_oauth2_provider())
    def put(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).get_health()

    @token_required(Config.get_oauth2_provider())
    def patch(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).get_health()

    @token_required(Config.get_oauth2_provider())
    def delete(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).get_health()


class UserDetailResource(UserResource):
    """ A specific user. """

    # @token_required(Config.get_oauth2_provider())
    def get(self, mci_id: str):
        return self.get_request_handler(request.headers).get_user_by_id(mci_id)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
