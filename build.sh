#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

python task_manager/manage.py collectstatic --no-input
python task_manager/manage.py migrate