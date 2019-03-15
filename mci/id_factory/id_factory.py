"""MCI ID Factory

This class implements a factory for producing MCI IDs. Why a factory? In the future
the algorithm for producing MCI IDs may need to be changed from the simplistic model
of relying directly on the Python UUID library. This ensures that the implementation
can be changed without adversely affecting the rest of the application it is best to
implement this feature with that need in mind.

"""

import uuid


class IDFactory(object):
    """MCI ID Factory.

    """

    @staticmethod
    def get_id():
        """Return a new MCI ID.

        Returns:
            string: The new MCI ID.

        """
        return str(uuid.uuid4()).replace('-', '')
