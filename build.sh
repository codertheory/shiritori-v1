#!/usr/bin/env bash

# Sets up the project for development

# Setup pre-commit
pre-commit install

# Setup Backend
(
    cd backend || exit
    poetry install
    poetry run python manage.py migrate
    poetry run python manage.py update_dictionary en
)

# Setup Frontend
(
    cd frontend || exit
    pnpm install
)

# exit
cd ..
exit 0
