#!/bin/bash

gunicorn -b 0.0.0.0 mci:app --reload