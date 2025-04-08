#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# wait-for-it.sh
# -----------------------------------------------------------------------------
# This script waits for a host and port to become available.
#
# Usage:
#   ./wait-for-it.sh host:port [-t timeout] [-- command args]
#
# Example:
#   ./wait-for-it.sh postgres:5432 -t 60 -- python main.py
#
# Source: https://github.com/vishnubob/wait-for-it
# -----------------------------------------------------------------------------

set -e

# Set default timeout to 60 seconds (overridden by -t flag)
TIMEOUT=60
QUIET=0
HOST=""
PORT=""
CMD=()

# Parse command line arguments.
while [[ $# -gt 0 ]]; do
  case "$1" in
    *:* )
      HOST=$(echo "$1" | cut -d: -f1)
      PORT=$(echo "$1" | cut -d: -f2)
      shift 1
      ;;
    -q|--quiet)
      QUIET=1
      shift 1
      ;;
    -t)
      TIMEOUT="$2"
      if [[ "$TIMEOUT" == "" ]]; then
        echo "Error: -t requires a timeout argument"
        exit 1
      fi
      shift 2
      ;;
    --)
      shift
      CMD=("$@")
      break
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$HOST" || -z "$PORT" ]]; then
  echo "Error: You must supply a host and port to test."
  exit 1
fi

if [[ $QUIET -eq 0 ]]; then
  echo "Waiting for $HOST:$PORT (timeout is $TIMEOUT seconds)..."
fi

start_ts=$(date +%s)
while true; do
  if nc -z "$HOST" "$PORT" 2>/dev/null; then
    break
  fi
  sleep 1
  current_ts=$(date +%s)
  if [[ $(( current_ts - start_ts )) -ge $TIMEOUT ]]; then
    echo "Timeout occurred after waiting $TIMEOUT seconds for $HOST:$PORT" >&2
    exit 1
  fi
done

if [[ $QUIET -eq 0 ]]; then
  elapsed=$(( $(date +%s) - start_ts ))
  echo "$HOST:$PORT is available after $elapsed seconds."
fi

if [ ${#CMD[@]} -gt 0 ]; then
  exec "${CMD[@]}"
fi
