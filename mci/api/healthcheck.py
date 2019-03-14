"""API Healthcheck Resource

This class represents a basic health check resource for providing clients with
quick status on the status of the API.

"""

from flask import request
from mci.api import VersionedResource, V1_0_0_HealthCheckHandler


class HealthCheckResource(VersionedResource):
    """Represents a simple health check resource.

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
            request_handler = V1_0_0_HealthCheckHandler()
        else:
            request_handler = V1_0_0_HealthCheckHandler()

        return request_handler

    def get(self):
        """ Handle GET request from API.

        Returns:
            dict: API health status.

        """
        return self.get_request_handler(request.headers).get_health()
