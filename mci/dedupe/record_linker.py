
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

training_file = 'mci/dedupe/data_matching_training.json'
settings_file = 'mci/dedupe/data_matching_learned_settings'

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
data_all_users = {
	'user1': {
		'first_name': 'Petey',
		'last_name': 'Jackson',
		'date_of_birth': None,
		'ssn': None
	},
	'user2': {
		'first_name': 'Janet',
		'last_name': 'Jack',
		'date_of_birth': None,
		'ssn': None
	},
	'user3': {
		'first_name': 'Frank',
		'last_name': 'Sinatra',
		'date_of_birth': None,
		'ssn': None
	},
	'user4': {
		'first_name': 'Nathan',
		'last_name': 'Jackson',
		'date_of_birth': None,
		'ssn': None
	},
	'user5': {
		'first_name': 'Nancy',
		'last_name': 'Jack',
		'date_of_birth': None,
		'ssn': None
	},
	'user6': {
		'first_name': 'Zora',
		'last_name': 'Sinatra',
		'date_of_birth': None,
		'ssn': None
	},
	'user7': {
		'first_name': 'Wendy',
		'last_name': 'Dolin',
		'date_of_birth': None,
		'ssn': None
	},
	'user8': {
		'first_name': 'Theo',
		'last_name': 'Kane',
		'date_of_birth': None,
		'ssn': None
	},
	'user9': {
		'first_name': 'Larry',
		'last_name': 'Name',
		'date_of_birth': None,
		'ssn': None
	}
}

data_posted_users = {
	'user1': {
		'first_name': 'Peter',
		'last_name': 'Jackson',
		'date_of_birth': None,
		'ssn': None
	},
	# 'user2': {
	# 	'first_name': 'Jesse',
	# 	'last_name': 'Yarn',
	# 	'date_of_birth': None,
	# 	'ssn': None
	# },
	# 'user3': {
	# 	'first_name': 'Steph',
	# 	'last_name': 'Sally',
	# 	'date_of_birth': None,
	# 	'ssn': None
	# },
	# 'user4': {
	# 	'first_name': 'Natham',
	# 	'last_name': 'Jackson',
	# 	'date_of_birth': None,
	# 	'ssn': None
	# },
	# 'user5': {
	# 	'first_name': 'Nancee',
	# 	'last_name': 'Jack',
	# 	'date_of_birth': None,
	# 	'ssn': None
	# },
	# 'user6': {
	# 	'first_name': 'Zorah',
	# 	'last_name': 'Sinatra',
	# 	'date_of_birth': None,
	# 	'ssn': None
	# }
}

# N.b., We want all fields in the Individual model, eventually.
fields = [
    {'field' : 'first_name', 'type': 'String'},
    {'field' : 'last_name', 'type': 'String'},
    {'field' : 'date_of_birth', 'type': 'DateTime',
     'has missing' : True},
    {'field' : 'ssn', 'type' : 'String', 'has missing' : True}]

# Create a new linker object and pass our data model to it.
if os.path.exists(settings_file):
    print('reading from', settings_file)
    with open(settings_file, 'rb') as sf :
        linker = dedupe.StaticRecordLink(sf)

else:
	linker = dedupe.RecordLink(fields)

	## Active learning: where does this happen? locally - so we can put it in version control?
	# Feed the linker object a sample of records.
	linker.sample(data_all_users, data_posted_users, 1000)

	# If we have training data saved from a previous run of linker,
    # look for it an load it in.
    # __Note:__ if you want to train from scratch, delete the training_file
    if os.path.exists(training_file):
        print('reading labeled examples from ', training_file)
        with open(training_file) as tf :
            linker.readTraining(tf)

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

import pdb; pdb.set_trace()

# do the matching
# returns:
# [(('user6', 'user6'), 1.0), (('user4', 'user4'), 0.9999986), (('user1', 'user1'), 0.9999904), (('user5', 'user5'), 0.9999814)]
linked_records = linker.match(data_all_users, data_posted_users, 0)

