#!/bin/sh
set -eu

mkdir -p /app/data

if [ ! -L /app/smartcrm.db ]; then
    if [ -f /app/smartcrm.db ]; then
        echo "ERROR: Existing database file blocks Docker volume link."
        exit 1
    fi
    ln -s /app/data/smartcrm.db /app/smartcrm.db
fi

python -m scripts.init_db

exec uvicorn src.backend.main:app --host 0.0.0.0 --port 8000
