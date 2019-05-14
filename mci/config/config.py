"""Application Configuration

A collection of classes for describing various application configuration environments.

"""

import os
import json
from brighthive_authlib import OAuth2ProviderFactory, AuthLibConfiguration


class Config(object):
    """Base configuration class.

    Note:
        This class is meant to be subclassed by all configuration objects.

    Class Attributes:
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): SQLAlchemy flag to determine
            whether or not track modifications should be enabled for PostgreSQL clients.

            Recommended default is False

        POSTGRES_USER (str): PostgreSQL username.

        POSTGRES_PASSWORD (str): PostgreSQL password.

        POSTGRES_DATABASE (str): PostgreSQL database name.

        POSTGRES_HOSTNAME (str): PostgreSQL hostname.

        POSTGRES_PORT (int): PostgreSQL port. Default port for PostgreSQL is 5432.

        SQLALCHEMY_DATABASE_URI (str): Connection string for PostgreSQL database. This string is comprised of the
            POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DATABASE, POSTGRES_HOSTNAME, and POSTGRES_PORT attributes

        RELATIVE_PATH (str): Relative path of the configuration file.

        ABSOLUTE_PATH (str): Absolute path of the configuration file.

        ROOT_PATH (str): The application root path computed from the difference between the relative path and the
            absolute path of the configuration file.

            Note:
                The purpose of this attribute is to ensure that the actual path where the application resides can
                easily be found regardless of where the application is currently being run.
    """

    RELATIVE_PATH = os.path.dirname(os.path.relpath(__file__))
    ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))

    # Calculate the root path of the application by subtracting the
    # relative path from the absolute path of this file.
    ROOT_PATH = ABSOLUTE_PATH.split(RELATIVE_PATH)[0]

    # Database Settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    POSTGRES_USER = 'test_user'
    POSTGRES_PASSWORD = 'test_password'
    POSTGRES_DATABASE = 'master_client_index'
    POSTGRES_HOSTNAME = 'localhost'
    POSTGRES_PORT = 5432
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOSTNAME,
        POSTGRES_PORT,
        POSTGRES_DATABASE
    )

    @staticmethod
    def get_settings():
        """Retrieve application settings from local settings file.

        Returns:
            dict: Settings retrieved from local `settings.json` file.

        """
        settings_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'settings.json')
        settings = {}

        if os.path.exists(settings_file) and os.path.isfile(settings_file):
            with open(settings_file, 'r') as f:
                settings = json.load(f)
        return settings

    @staticmethod
    def get_data_resource_url():
        """Retrieve the Data Resource API URL.

        Returns:
            str: Data Resource API URL

        """
        return os.getenv('DATA_RESOURCE_URL', 'http://localhost:5000')

    @staticmethod
    def get_matching_service_uri():
        """Retrieves the URI for the mci-matching-service, which
        listens for POST requests from MCI and returns a potential user 
        and match score.

        The matching service runs in a container, on the same Docker network as MCI,
        and it can be accessed via the mci-matching-service container name.
        """
        return os.getenv('MATCHING_SERVICE_URI', 'http://mcimatchingservice_mci_1:8000/compute-match')

    @staticmethod
    def get_api_version():
        """Return API version.

        Returns:
            str: API version.
                Note:
                    If the API version cannot be found, it will return the text 'Unknown'

        """
        api_version = 'Unknown'
        try:
            api_version = str(Config.get_settings()['API_VERSION']).strip()
        except KeyError:
            pass

        return api_version

    @staticmethod
    def get_api_name():
        """Return API name.

        Returns:
            str: API name.
                Note:
                    If the API name cannot be found, it will return the text 'Unknown'

        """
        api_name = 'Unknown'
        try:
            api_name = str(Config.get_settings()['API_NAME']).strip()
        except KeyError:
            pass

        return api_name

    @staticmethod
    def get_oauth2_provider():
        """Get the OAuth 2.0 provider.

        """
        # OAuth 2.0
        provider = 'AUTH0'
        oauth2_url = 'https://brighthive-test.auth0.com'
        json_url = '{}/.well-known/jwks.json'.format(oauth2_url)
        audience = 'http://localhost:8000'
        algorithms = ['RS256']
        auth_config = AuthLibConfiguration(
            provider=provider, base_url=oauth2_url, jwks_url=json_url, algorithms=algorithms, audience=audience)
        oauth2_provider = OAuth2ProviderFactory.get_provider(
            provider, auth_config)
        return oauth2_provider

class DevelopmentConfig(Config):
    """Development Configuration class.

    This class provides the configuration necessary for the `development` environment.

    Class Attributes:
        CONTAINER_NAME (str): Label for the Docker container for the PostgreSQL container.

        IMAGE_NAME (str): Name of the Docker image for the PostgreSQL database.

        IMAGE_VERSION (str): Version of the Docker image for the PostgreSQL database.

        POSTGRES_PORT (int): PostgreSQL port.

        SQLALCHEMY_DATABASE_URI (str): Connection string for PostgreSQL database.
    """

    def __init__(self):
        super().__init__()
        os.environ['FLASK_ENV'] = 'development'

    CONTAINER_NAME = 'postgres-dev'
    IMAGE_NAME = 'postgres'
    IMAGE_VERSION = '11.2'
    POSTGRES_DATABASE = 'master_client_index_dev'
    POSTGRES_PORT = 5432
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        Config.POSTGRES_USER,
        Config.POSTGRES_PASSWORD,
        Config.POSTGRES_HOSTNAME,
        POSTGRES_PORT,
        POSTGRES_DATABASE
    )

    def get_postgresql_image(self):
        """Provide the name of the PostgreSQL Docker image to load for development.

        Returns:
            str: Name and version of the PostgreSQL Docker image to load.

        """
        return '{}:{}'.format(self.IMAGE_NAME, self.IMAGE_VERSION)

class TestConfig(Config):
    """Test Configuration class.

    This class provides the configuration necessary for the `testing` environment.

    Class Attributes:
        CONTAINER_NAME (str): Label for the Docker container for the PostgreSQL container.

        IMAGE_NAME (str): Name of the Docker image for the PostgreSQL database.

        IMAGE_VERSION (str): Version of the Docker image for the PostgreSQL database.

        POSTGRES_DATABASE (str): PostgreSQL database name.

        POSTGRES_PORT (int): PostgreSQL port.

        SQLALCHEMY_DATABASE_URI (str): Connection string for PostgreSQL database.
    """

    def __init__(self):
        super().__init__()
        os.environ['FLASK_ENV'] = 'testing'

    CONTAINER_NAME = 'postgres-test'
    IMAGE_NAME = 'postgres'
    IMAGE_VERSION = '11.2'
    POSTGRES_DATABASE = 'master_client_index_test'
    POSTGRES_PORT = 5433
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        Config.POSTGRES_USER,
        Config.POSTGRES_PASSWORD,
        Config.POSTGRES_HOSTNAME,
        POSTGRES_PORT,
        POSTGRES_DATABASE
    )

    def get_postgresql_image(self):
        """Provide the name of the PostgreSQL Docker image to load for testing.

        Returns:
            str: Name and version of the PostgreSQL Docker image to load.

        """
        return '{}:{}'.format(self.IMAGE_NAME, self.IMAGE_VERSION)


class SandboxConfig(Config):
    """Sandbox configuration class.

    This class provides the configuration necessary for the `sandbox` environment.

    Class Attributes:
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): SQLAlchemy flag to determine
            whether or not track modifications should be enabled for PostgreSQL clients.

            Recommended default is False

        POSTGRES_USER (str): PostgreSQL username.

        POSTGRES_PASSWORD (str): PostgreSQL password.

        POSTGRES_DATABASE (str): PostgreSQL database name.

        POSTGRES_HOSTNAME (str): PostgreSQL hostname.

        POSTGRES_PORT (int): PostgreSQL port.

        SQLALCHEMY_DATABASE_URI (str): Connection string for PostgreSQL database. This string is comprised of the
            POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DATABASE, POSTGRES_HOSTNAME, and POSTGRES_PORT attributes
    """

    def __init__(self):
        super().__init__()
        os.environ['FLASK_ENV'] = 'production'

    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
    POSTGRES_HOSTNAME = os.getenv('POSTGRES_HOSTNAME')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOSTNAME,
        POSTGRES_PORT,
        POSTGRES_DATABASE
    )


class ProductionConfig(Config):
    """Production configuration class.

    This class provides the configuration necessary for the `production` environment.

    """

    def __init__(self):
        super().__init__()
        os.environ['FLASK_ENV'] = 'production'


class IntegrationTestConfig(Config):
    """Integration Testing configuration class.

    This class provides the configuration necessary for the `integration_testing` environment.

    Note:
        The key difference between this class and the TestConfig class is that TestConfig is purpose-built
        for unit testing.

    Class Attributes:
        POSTGRES_DATABASE (str): PostgreSQL database name.
        POSTGRES_PORT (int): PostgreSQL port.

        SQLALCHEMY_DATABASE_URI (str): Connection string for PostgreSQL database. This string is comprised of the
            POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DATABASE, POSTGRES_HOSTNAME, and POSTGRES_PORT attributes
    """

    def __init__(self):
        super().__init__()
        os.environ['FLASK_ENV'] = 'testing'

    POSTGRES_DATABASE = 'master_client_index_integration'
    POSTGRES_PORT = 5432
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
        Config.POSTGRES_USER,
        Config.POSTGRES_PASSWORD,
        Config.POSTGRES_HOSTNAME,
        POSTGRES_PORT,
        POSTGRES_DATABASE
    )


class ConfigurationFactory(object):
    """Application configuration factory.

    This factoty class provides a quick and easy mechanism for retrieving a specific configuration
    type without the need for manually creating configuration objects.

    """

    @staticmethod
    def get_config(config_type: str):
        """Return a configuration by it's type.

        Primary factory method that returns a configuration object based on the provided configuration type.

        Args:
            config_type (str): Configuration factory type return. May be one of:
                - TEST
                - DEVELOPMENT
                - INTEGRATION
                - SANDBOX
                - PRODUCTION

        Returns:
            object: Configuration object based on the specified config_type.

        """
        if config_type.upper() == 'TEST':
            return TestConfig()
        elif config_type.upper() == 'DEVELOPMENT':
            return DevelopmentConfig()
        elif config_type.upper() == 'SANDBOX':
            return SandboxConfig()
        elif config_type.upper() == 'INTEGRATION':
            return IntegrationTestConfig()
        elif config_type.upper() == 'PRODUCTION':
            return ProductionConfig()

    @staticmethod
    def from_env():
        """Retrieve configuration based on environment settings.

        Provides a configuration object based on the settings found in the `APP_ENV` variable. Defaults to the `development`
        environment if the variable is not set.

        Returns:
            object: Configuration object based on the configuration environment found in the `APP_ENV` environment variable.

        """
        environment = os.getenv('APP_ENV', 'DEVELOPMENT')
        return ConfigurationFactory.get_config(environment)
