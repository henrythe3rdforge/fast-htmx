#!/bin/bash
# Manage all generated services

PID_FILE="services.pid"

case "$1" in
    list|ls|"")
        echo "Services:"
        [ ! -f "$PID_FILE" ] && echo "  (none)" && exit 0
        while IFS=: read -r name pid port; do
            [ -z "$name" ] && continue
            kill -0 "$pid" 2>/dev/null && echo "  $name — http://localhost:$port (PID $pid)" || echo "  $name — dead"
        done < "$PID_FILE"
        ;;
    stop)
        [ -n "$2" ] && [ -d "$2" ] && (cd "$2" && ./stop.sh) && exit 0
        [ ! -f "$PID_FILE" ] && echo "Nothing to stop" && exit 0
        while IFS=: read -r name pid port; do
            [ -n "$pid" ] && kill "$pid" 2>/dev/null && echo "Stopped $name"
        done < "$PID_FILE"
        rm -f "$PID_FILE"
        ;;
    start)
        [ -n "$2" ] && [ -d "$2" ] && (cd "$2" && ./start.sh) && exit 0
        for d in */; do [ -f "${d}start.sh" ] && (cd "$d" && ./start.sh); done
        ;;
    *)
        echo "Usage: $0 [list|start|stop] [service]"
        ;;
esac
