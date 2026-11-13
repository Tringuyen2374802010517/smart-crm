#!/bin/sh

set -eu

if [ ! -L /app/smartcrm.db ]; then
    echo "ERROR: Database symlink is missing."
    exit 1
fi

if [ ! -d /app/data ]; then
    echo "ERROR: Database volume is not mounted."
    exit 1
fi

chown -R appuser:appuser /app/data
chmod 700 /app/data

if [ -f /app/data/smartcrm.db ]; then
    chmod 600 /app/data/smartcrm.db
fi

echo "PASS: Database permissions configured."

gosu appuser python -m scripts.init_db

exec gosu appuser uvicorn \
    src.backend.main:app \
    --host 0.0.0.0 \
    --port 8000
