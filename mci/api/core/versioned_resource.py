"""Versioned API Resource

This class extends the Flask-Restful Resource class with the ability to
identify the API version number in a request header.

"""

from flask_restful import Resource


class VersionedResource(Resource):
    """Represents a version-aware RESTful Resource.

    """

    def __init__(self):
        super().__init__()

    def get_api_version(self, headers):
        """Retrieve the API version from the HTTP request header.

        Args:
            headers (dict): HTTP request headers passed in by the client.

        Returns:
            str: The API version number, defaulted to the oldest supported version number
                 if the header was not provided.

        """
        try:
            api_version = headers['X-Api-Version']
        except KeyError:
            api_version = '1.0.0'

        return api_version

    def get_request_handler(self, headers):
        """Retrieve request handler based on API version number.

        Note:
            This method should be overridden by children classes in order to
            provide the appropriate request handler based on version number.

        Args:
            headers (dict): HTTP request headers passed in by the client.

        Returns:
            object: API request handler based on version number.

        """
        pass
