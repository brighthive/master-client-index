"""Health Check Handler

Handle health check requests from the API.

"""

from datetime import datetime


class HealthCheckHandler(object):
    """Health Check Handler.

    """

    def get_health(self):
        """ Returns basic API health check information.

        Returns:
            dict: API health check status and other details.
            int: HTTP Status Code

        """
        return {
            'api_name': 'BrightHive Master Client Index API',
            'current_time': str(datetime.utcnow()),
            'current_api_version': '1.0.0',
            'api_status': 'OK'
        }, 200
