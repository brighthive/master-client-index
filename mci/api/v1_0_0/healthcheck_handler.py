"""Health Check Handler

Handle health check requests from the API.

"""

from datetime import datetime

from mci_database.db import db
from mci_database.db.models import (Address, Disposition, EducationLevel,
                                    EmploymentStatus, EthnicityRace, Gender,
                                    Individual, IndividualDisposition, Source)


class HealthCheckHandler(object):
    """Health Check Handler.

    """

    def get_health(self):
        """ Returns basic API health check information.

        Returns:
            dict: API health check status and other details.
            int: HTTP Status Code

        """

        # TODO: Wrap these in try-except blocks, and determine the "health".
        individuals = Individual.query.count()
        addresses = Address.query.count()
        dispositions = Disposition.query.count()
        education_levels = EducationLevel.query.count()
        employment_statuses = EmploymentStatus.query.count()
        ethnicities = EthnicityRace.query.count()
        genders = Gender.query.count()
        sources = Source.query.count()

        return {
            'api_name': 'BrightHive Master Client Index API',
            'current_time': str(datetime.utcnow()),
            'current_api_version': '1.0.0',
            'api_status': 'OK',
            'endpoints': {
                'individuals': {
                    'count': individuals,
                    'health': 'OK'
                },
                'addresses': {
                    'count': addresses,
                    'health': 'OK'
                },
                'dispositions': {
                    'count': dispositions,
                    'health': 'OK'
                },
                'education_levels': {
                    'count': education_levels,
                    'health': 'OK'
                },
                'employment_statuses': {
                    'count': employment_statuses,
                    'health': 'OK'
                },
                'ethnicities': {
                    'count': ethnicities,
                    'health': 'OK'
                },
                'genders': {
                    'count': genders,
                    'health': 'OK'
                },
                'sources': {
                    'count': sources,
                    'health': 'OK'
                }
            }
        }, 200
