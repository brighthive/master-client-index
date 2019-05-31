#!/bin/bash

MAX_RETRIES=5

# The Pipfile specifes "editable = true" (otherwise, Pip does not install non-Python files).
MIGRATION_PATH="/master-client-index/src/mci-database/mci_database/db/migrations"

if [ "$APP_ENV" == "SANDBOX" ]; then
    RETRIES=0
    until flask db upgrade -d $MIGRATION_PATH; do
        RETRIES=`expr $RETRIES + 1`
        if [[ "$RETRIES" -eq "$MAX_RETRIES" ]]; then
            echo "Retry Limit Exceeded. Aborting..."
            exit 1
        fi
        sleep 2
    done
fi

if [ "$APP_ENV" == "DEVELOPMENT" ] || [ -z "$APP_ENV" ]; then
    gunicorn -b 0.0.0.0 wsgi --reload
else
    gunicorn -b 0.0.0.0 wsgi
fi