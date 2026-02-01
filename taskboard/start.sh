#!/bin/bash
cd "$(dirname "$0")"
NAME="taskboard"

# Check if running
[ -f app.pid ] && kill -0 $(cat app.pid) 2>/dev/null && echo "$NAME already running" && exit 1

# Setup venv
[ ! -d venv ] && python3 -m venv venv && venv/bin/pip install -q -r requirements.txt

# Download HTMX if missing
[ ! -f static/js/htmx.min.js ] && curl -sL -o static/js/htmx.min.js https://unpkg.com/htmx.org@2.0.4/dist/htmx.min.js

# Find free port
PORT=$(python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1]); s.close()")

# Start
export PORT
nohup venv/bin/uvicorn app:app --host 0.0.0.0 --port $PORT --workers 2 > app.log 2>&1 &
echo $! > app.pid
echo $PORT > app.port

echo "$NAME started at http://localhost:$PORT"
