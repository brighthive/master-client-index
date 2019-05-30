from setuptools import setup, find_packages

setup(
    name='mci',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'flask', 
        'flask-sqlalchemy',
        'pycodestyle',
        'autopep8',
        'flask',
        'flask-restful',
        'gunicorn',
        'flask-sqlalchemy',
        'flask-migrate',
        'psycopg2-binary',
        'brighthive-authlib'
    ],
)
