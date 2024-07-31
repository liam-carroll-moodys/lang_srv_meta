#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Navigate to the installation directory
cd /nwsys/translation_srv

# Activate virtual environment
source venv/bin/activate

# Run the application
exec gunicorn --bind 0.0.0.0:5007 app.index:app

# Note: Ensure this script has the correct permissions:
# sudo chmod 750 /nwsys/translation_srv/scripts/run.sh
# sudo chown nadmin:amc /nwsys/translation_srv/scripts/run.sh