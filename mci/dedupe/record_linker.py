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

## Query database for all Individuals 
# (n.b., I could not connect to the db with sqlalchemy – something seems to be wrong with my string)
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

## For testing – hardcode some data..
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
	'user2': {
		'first_name': 'Jesse',
		'last_name': 'Yarn',
		'date_of_birth': None,
		'ssn': None
	},
	'user3': {
		'first_name': 'Steph',
		'last_name': 'Sally',
		'date_of_birth': None,
		'ssn': None
	},
	'user4': {
		'first_name': 'Natham',
		'last_name': 'Jackson',
		'date_of_birth': None,
		'ssn': None
	},
	'user5': {
		'first_name': 'Nancee',
		'last_name': 'Jack',
		'date_of_birth': None,
		'ssn': None
	},
	'user6': {
		'first_name': 'Zorah',
		'last_name': 'Sinatra',
		'date_of_birth': None,
		'ssn': None
	}
}

## Instantiate a new RecordLink (for merging two datasets)
# https://docs.dedupe.io/en/latest/API-documentation.html#recordlink-objects
# https://docs.dedupe.io/en/latest/API-documentation.html#staticrecordlink-objects
# A RecordLink (or StaticRecordLink) requires a list of variables/fields used for training the model.
# The RecordLink takes a list of dicts. 
# The StaticRecordLink takes settings/training data produced from a previously active RecordLink instance.
# QUESTION: how big are the VA and CO Individual tables, i.e., do we need to create "blocks"?


## FOR REFACTOR in USER_HANDLER.PY
## Expects existing trained data (what happens if trained data is not there? raise an error, no?)
if os.path.exists(settings_file):
    print('reading from', settings_file)
    with open(settings_file, 'rb') as sf:
        linker = dedupe.StaticRecordLink(sf)

## FOR A MANAGEMENT COMMAND THAT PRODUCES THE TRAINING DATA
# To be run by a BrightHive dev.
# QUESTION: when should we run the management script? maybe locally, then push it into the version control? (that requires a BrightHive dev to have a full dataset on their local machine...)
# QUESTION: how much sample data do we need, i.e.
# is one db (just VA, just CO) enough?
else:
	## Define fields
	# QUESTION: Which fields should we match? We could start with the five described in the original algorithm?
	# Or do we want dededupe to consider all fields? 
	# TODO: research if more-or-less fields make a difference...
	fields = [
		{'field' : 'first_name', 'type': 'String'},
		{'field' : 'last_name', 'type': 'String'},
		{'field' : 'date_of_birth', 'type': 'DateTime',
		 'has missing' : True},
		{'field' : 'ssn', 'type' : 'String', 'has missing' : True}]

	linker = dedupe.RecordLink(fields)

	## Active learning: where does this happen? locally - so we can put it in version control?
	# Feed the linker object a sample of records.
	linker.sample(data_all_users, data_posted_users, 1000)

	# If we have training data saved from a previous run of linker,
    # look for it and load it in.
    # __Note:__ if you want to train from scratch, delete the training_file
	if os.path.exists(training_file):
		print('reading labeled examples from ', training_file)
		with open(training_file) as tf:
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

# do the matching
# returns:
# [(('user6', 'user6'), 1.0), (('user4', 'user4'), 0.9999986), (('user1', 'user1'), 0.9999904), (('user5', 'user5'), 0.9999814)]
linked_records = linker.match(data_all_users, data_posted_users, 0)
print("Hurrah!", linked_records)

