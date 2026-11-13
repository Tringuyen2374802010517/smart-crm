#!/usr/bin/env bash
set -euo pipefail

if [ ! -L /app/smartcrm.db ]; then
    echo "ERROR: SQLite symlink missing."
    exit 1
fi

if [ ! -d /app/data ]; then
    echo "ERROR: SQLite data directory missing."
    exit 1
fi

chown -R appuser:appuser /app/data
chmod 700 /app/data

if [ -f /app/data/smartcrm.db ]; then
    chmod 600 /app/data/smartcrm.db
fi

gosu appuser python -m scripts.init_db

gosu appuser uvicorn src.backend.main:app \
    --host 127.0.0.1 \
    --port 8000 &
API_PID=$!

nginx -g 'daemon off;' &
NGINX_PID=$!

shutdown() {
    kill "$API_PID" "$NGINX_PID" 2>/dev/null || true
    wait "$API_PID" "$NGINX_PID" 2>/dev/null || true
}

trap shutdown EXIT
trap 'exit 143' TERM
trap 'exit 130' INT

wait -n "$API_PID" "$NGINX_PID"
echo "ERROR: One of the application processes exited."
exit 1
