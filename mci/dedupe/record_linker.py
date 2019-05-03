
from __future__ import print_function
from future.builtins import next

import os
import csv
import re
import collections
import logging
import optparse
import numpy

import dedupe
from unidecode import unidecode

from sqlalchemy import create_engine

POSTGRES_USER = 'brighthive'
POSTGRES_PASSWORD = 'test_password'
POSTGRES_DATABASE = 'mci_dev'
POSTGRES_HOSTNAME = 'masterclientindex_postgres_mci_1'
POSTGRES_PORT = 5432

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOSTNAME,
    POSTGRES_PORT,
    POSTGRES_DATABASE
)

engine = create_engine(SQLALCHEMY_DATABASE_URI, 
                       convert_unicode=True)

# data_database = engine.execute("select * from individual").fetchall()

# Data should be a nested dict, where each key represents a user, and
# the value represents a dict of attributes.
# {'AbtBuy_Buy.csv1090': {'unique_id': '1075', 'title': 'iwork 09 family packint dvd mb943z a', 'description': None, 'price': None}, 
# 'AbtBuy_Buy.csv1091': {'unique_id': '1076', 'title': 'case mate carbon fiber iphone 3g case black iph3gcbcf', 'description': None, 'price': 28.08}}
data_all_users = {
	'user': {
		'first_name': 'Petey',
		'last_name': 'Jackson',
		'date_of_birth': '',
		'ssn': '',
	}
}

data_posted_user = {
	'posted_user': {
		'first_name': 'Peter',
		'last_name': 'Jackson',
		'date_of_birth': '',
		'ssn': '',
	}
}

# N.b., We want all fields in the Individual model, eventually.
fields = [
    {'field' : 'first_name', 'type': 'String'},
    {'field' : 'last_name', 'type': 'String'},
    {'field' : 'date_of_birth', 'type': 'DateTime',
     'has missing' : True},
    {'field' : 'ssn', 'type' : 'String', 'has missing' : True}]



# Create a new linker object and pass our data model to it.
linker = dedupe.RecordLink(fields)

## Active learning: where does this happen? locally - so we can put it in version control?
# Feed the linker object a sample of records.
linker.sample(data_all_users, data_posted_user)
dedupe.consoleLabel(linker)
linker.train()

# When finished, save our training away to disk
with open(training_file, 'w') as tf :
    linker.writeTraining(tf)

# Save our weights and predicates to disk.  If the settings file
# exists, we will skip all the training and learning next time we run
# this file.
with open(settings_file, 'wb') as sf :
    linker.writeSettings(sf)


# do the matching
linked_records = linker.match(data_1, data_2, 0)
