"""Test Fixtures

Contains all PyTest fixtures shared across multiple unit tests in the tests module.

"""

import os
from time import sleep

import docker
import pytest
from flask_migrate import upgrade

from mci import create_app
from mci.config import ConfigurationFactory
from mci_database import db
from mci_database.db.models import (Address, Disposition, EducationLevel,
                                    EmploymentStatus, EthnicityRace, Gender,
                                    Individual)

environment = os.getenv('APP_ENV', 'TEST')
config = ConfigurationFactory.get_config(environment.upper())
app = create_app()
app.config.from_object(config)

MAX_RETRIES = 10  # number of times to retry migrations before giving up
SLEEP = 2  # sleep interval (seconds) between retries of migration


def apply_migrations():
    """Apply Database Migrations

    Applies the database migrations to the test database container.

    Args:
        config (object): Configuration object to pull the needed components from.

    """
    applied_migrations = False
    retries = 0

    with app.app_context():
        # The migrations repo resides in the virtual env.
        # Specifically, Pipenv installs the mci-database repo in the `src` directory,
        # since the Pipfile marks it as "editable."
        path_to_virtual_env = os.environ['VIRTUAL_ENV']
        migrations_dir = os.path.join(
            path_to_virtual_env, 'src', 'mci-database', 'mci_database', 'db', 'migrations')

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

    apply_migrations()


def teardown_postgres_container():
    """Teardown Dockerr PostgreSQL container.

    Spins down the Docker PostgreSQL testing container.

    """
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


@pytest.fixture(scope="session")
def app_context():
    with app.app_context() as context:
        yield context

def _individual():
    individual = {
        'first_name': 'Nicola',
        'last_name': 'Haym',
        'middle_name': 'Francesco',
        'date_of_birth': '1678-07-06',
        'email_address': 'nicola@ram.uk',
        'telephone': '999-124-5678'
    }

    return individual

@pytest.fixture
def individual_data():
    '''
    Returns a blob of data. 
    Ideal for POSTing an individual to the `users` endpoint.
    '''
    return _individual()

@pytest.fixture
def individual_obj(database, mailing_address_obj, app_context):
    '''
    Populates the database with an Individual and returns its MCI ID.
    '''
    individual_obj = Individual(**_individual())
    individual_obj.mailing_address_id = 1
    mci_id = individual_obj.mci_id

    database.session.add(individual_obj) 
    database.session.commit()
        
    return mci_id
    
@pytest.fixture
def mailing_address_obj(database, app_context):
    address_data = {
        'address': '25 Brook St',
        'city': 'London',
    }

    mailing_address_obj = Address(**address_data)

    database.session.add(mailing_address_obj) 
    database.session.commit()
    
    return mailing_address_obj

@pytest.fixture
def gender_obj(database, app_context):
    gender_obj = Gender(gender='Female')

    database.session.add(gender_obj) 
    database.session.commit()
    
    return gender_obj

@pytest.fixture
def ethnicity_obj(database, app_context):
    ethnicity_obj = EthnicityRace(ethnicity_race='Alaska Native')

    database.session.add(ethnicity_obj) 
    database.session.commit()
    
    return ethnicity_obj

@pytest.fixture
def education_obj(database, app_context):
    education_obj = EducationLevel(education_level='Masters')

    database.session.add(education_obj) 
    database.session.commit()
    
    return education_obj

@pytest.fixture
def employment_obj(database, app_context):
    employment_obj = EmploymentStatus(employment_status='Employed')

    database.session.add(employment_obj) 
    database.session.commit()
    
    return employment_obj

@pytest.fixture
def disposition_obj(database, app_context):
    disposition_obj = Disposition(disposition='student')

    database.session.add(disposition_obj) 
    database.session.commit()
    
    return disposition_obj

@pytest.fixture
def json_headers():
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    return headers

@pytest.fixture
def test_client(scope='module'):
    return app.test_client()