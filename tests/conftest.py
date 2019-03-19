"""Test Fixtures

Contains all PyTest fixtures shared across multiple unit tests in the tests module.

"""

import os
import pytest
import docker
from flask_migrate import upgrade
from time import sleep
from mci.config import ConfigurationFactory
from mci import app, db

MAX_RETRIES = 10  # number of times to retry migrations before giving up
SLEEP = 2  # sleep interval (seconds) between retries of migration


def apply_migrations(config):
    """Apply Database Migrations

    Applies the database migrations to the test database container.

    Args:
        config (object): Configuration object to pull the needed components from.

    """
    applied_migrations = False
    retries = 0

    app.config.from_object(config)
    with app.app_context():
        # determine the path of the migrations directory
        relative_path = os.path.dirname(os.path.relpath(__file__))
        absolute_path = os.path.dirname(os.path.abspath(__file__))
        root_path = absolute_path.split(relative_path)[0]
        migrations_dir = os.path.join(
            root_path, 'mci', 'db', 'migrations')

        while retries < MAX_RETRIES and applied_migrations is False:
            print('Attempting to apply migrations ({} of {})...'.format(
                retries + 1, MAX_RETRIES))
            try:
                # apply the migrations
                upgrade(directory=migrations_dir)
                applied_migrations = True
            except Exception:
                retries += 1
                sleep(SLEEP)


def setup_postgres_container():
    """Setup Docker PostgreSQL container.

    Spins up a Docker PostgreSQL container for testing.

    """

    environment = os.getenv('APP_ENV', 'TEST')
    config = ConfigurationFactory.get_config(environment.upper())
    docker_client = docker.from_env()

    # download Docker PostgreSQL image for unit testing only
    if environment.upper() != 'INTEGRATION':
        try:
            print('Launching Docker PostgreSQL Container...')
            docker_client.images.pull(config.get_postgresql_image())
        except Exception:
            print('Failed to retrieve PostgreSQL image {}'.format(
                config.get_postgresql_image()))

    # launch Docker PostgreSQL image for unit testing only
    if environment.upper() != 'INTEGRATION':
        db_environment = [
            'POSTGRES_USER={}'.format(config.POSTGRES_USER),
            'POSTGRES_PASSWORD={}'.format(config.POSTGRES_PASSWORD),
            'POSTGRES_DB={}'.format(config.POSTGRES_DATABASE)
        ]
        try:
            docker_client.containers.run(
                config.get_postgresql_image(),
                detach=True,
                auto_remove=True,
                name=config.CONTAINER_NAME,
                ports={'5432/tcp': config.POSTGRES_PORT},
                environment=db_environment
            )
        except Exception:
            print('Unable to start container {}...'.format(config.CONTAINER_NAME))

    apply_migrations(config)


def teardown_postgres_container():
    """Teardown Dockerr PostgreSQL container.

    Spins down the Docker PostgreSQL testing container.

    """
    environment = os.getenv('APP_ENV', 'TEST')
    if environment.upper() != 'INTEGRATION':
        print('Tearing Down Docker PostgreSQL Container...')
        config = ConfigurationFactory.get_config(environment.upper())
        docker_client = docker.from_env()
        try:
            container = docker_client.containers.get(config.CONTAINER_NAME)
            container.stop()
        except Exception:
            print('Unable to stop container {}...'.format(config.CONTAINER_NAME))


@pytest.fixture(scope='session')
def database():
    """Database fixture."""
    setup_postgres_container()
    yield db
    teardown_postgres_container()


@pytest.fixture
def test_client(scope='module'):
    return app.test_client()
