#!/usr/bin/env bash
set -euo pipefail

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt -q

if [ ! -f "config.yaml" ]; then
  cp config.example.yaml config.yaml
  echo >&2 "Please edit config.yaml with your settings and run the script again."
  exit 1
fi

mkdir -p data logs

python3 -m src.server.server "$@"