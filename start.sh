#!/bin/bash
if [[ ! -v NUMBER_OF_WORKERS ]]; then
    export NUMBER_OF_WORKERS=$(grep -c processor /proc/cpuinfo)
fi

. /app/.venv/bin/activate

gunicorn --workers ${NUMBER_OF_WORKERS} --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker server:app