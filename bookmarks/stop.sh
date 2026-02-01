#!/bin/bash
cd "$(dirname "$0")"
NAME="bookmarks"
PID_FILE="../services.pid"

[ ! -f app.pid ] && echo "$NAME not running" && exit 0

PID=$(cat app.pid)
kill $PID 2>/dev/null; sleep 1; kill -0 $PID 2>/dev/null && kill -9 $PID 2>/dev/null
rm -f app.pid app.port

# Clean parent PID file
[ -f "$PID_FILE" ] && grep -v "^${NAME}:" "$PID_FILE" > "$PID_FILE.tmp" && \
  ([ -s "$PID_FILE.tmp" ] && mv "$PID_FILE.tmp" "$PID_FILE" || rm -f "$PID_FILE" "$PID_FILE.tmp")

echo "$NAME stopped"
