#!/bin/bash

# script/bootstrap: Resolve all dependencies the application requires to run.

set -e

cd "$(dirname "$BASH_SOURCE")/.."

hash pipenv 2>/dev/null || {
    echo >&2 "Command 'pipenv' not found. Aborting."
    exit 1
}

PIPENV_VENV_IN_PROJECT=1 pipenv install --dev --skip-lock
