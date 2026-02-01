#!/bin/bash
cd "$(dirname "$0")"
NAME="bookmarks"

if [ -f app.pid ] && kill -0 $(cat app.pid) 2>/dev/null; then
    echo "$NAME running at http://localhost:$(cat app.port) (PID: $(cat app.pid))"
else
    rm -f app.pid app.port
    echo "$NAME not running"
    exit 1
fi
