#!/bin/bash

MAX_RETRIES=5
MIGRATION_PATH=mci/db/migrations

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
    gunicorn -b 0.0.0.0 mci:app --reload
else
    gunicorn -b 0.0.0.0 mci:app --reload --log-level=DEBUG --timeout 240
fi