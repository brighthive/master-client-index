"""Test Fixtures

Contains all PyTest fixtures shared across multiple unit tests in the tests module.

"""

import pytest
import docker
from mci.config import ConfigurationFactory


def setup_postgres_container():
    """Setup Docker PostgreSQL container.

    Spins up a Docker PostgreSQL container for testing.

    """
    print('Spinning Up Docker Container.....')
    docker_client = docker.from_env()
    docker_client.containers.run(
        'postgres:11.2',
        detach=True,
        auto_remove=True,
        name='postgres_test',
        ports={'5432/tcp': '5433'}
    )


def teardown_postgres_container():
    """Teardown Dockerr PostgreSQL container.

    Spins down the Docker PostgreSQL testing container.

    """
    print('Tearing Down Docker Container...')
    docker_client = docker.from_env()
    container = docker_client.containers.get('postgres_test')
    container.stop()


@pytest.fixture(scope='session')
def database():
    """Database fixture."""
    setup_postgres_container()
    yield {'status': 'ok'}
    teardown_postgres_container()
