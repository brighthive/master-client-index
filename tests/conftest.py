"""Test Fixtures

Contains all PyTest fixtures shared across multiple unit tests in the tests module.

"""

import pytest


@pytest.fixture(scope='module')
def database():
    """Database fixture."""
    return {'status': 'ok'}
