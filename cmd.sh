#!/bin/bash

MAX_RETRIES=5
WORKERS=4

# The Pipfile specifes "editable = true" (otherwise, Pip does not install non-Python files).
MIGRATION_PATH="/master-client-index/src/mci-database/mci_database/db/migrations"

RETRIES=0
until flask db upgrade -d $MIGRATION_PATH; do
    RETRIES=`expr $RETRIES + 1`
    if [[ "$RETRIES" -eq "$MAX_RETRIES" ]]; then
        echo "Retry Limit Exceeded. Aborting..."
        exit 1
    fi
    sleep 2
done

if [ "$APP_ENV" == "DEVELOPMENT" ] || [ -z "$APP_ENV" ]; then
    gunicorn -b 0.0.0.0 wsgi --reload --log-level=DEBUG --timeout 240 --worker-class gevent
else
    gunicorn -b 0.0.0.0 wsgi --workers=$WORKERS --worker-class gevent
fi
