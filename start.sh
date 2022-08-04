#!/bin/bash
if [[ ! -v NUMBER_OF_WORKERS ]]; then
    export NUMBER_OF_WORKERS=$(grep -c processor /proc/cpuinfo)
fi

uvicorn api.server:app --host 0.0.0.0 --port 8000 --workers ${NUMBER_OF_WORKERS}