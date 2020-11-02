#!/bin/bash
set -e
pwd

echo "Starting SSH ..."
service ssh start

python /code/runserver.py