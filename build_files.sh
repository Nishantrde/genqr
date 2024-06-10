#!/bin/bash

# Ensure script stops on error
set -e

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install Python packages from requirements.txt
pip install -r requirements.txt

# Add any other necessary build steps below
# For example, if you need to run database migrations or collect static files for Django:
# python manage.py migrate
# python manage.py collectstatic --noinput

echo "Build script completed successfully."
