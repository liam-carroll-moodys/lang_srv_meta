#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Set the installation path
INSTALL_PATH="/nwsys/translation_srv"

# Create the installation directory if it doesn't exist
mkdir -p $INSTALL_PATH

# Copy all files to the installation directory
cp -R ../ $INSTALL_PATH

# Navigate to the installation directory
cd $INSTALL_PATH

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt')"

# Setup systemd service
cp scripts/translation-service.service /etc/systemd/system/
sed -i "s|REPLACE_WITH_YOUR_USERNAME|nadmin|g" /etc/systemd/system/translation-service.service
sed -i "s|REPLACE_WITH_YOUR_GROUP|amc|g" /etc/systemd/system/translation-service.service
sed -i "s|/path/to/translation-service|$INSTALL_PATH|g" /etc/systemd/system/translation-service.service
systemctl daemon-reload
systemctl enable translation-service

# Set ownership of the installation directory to nadmin:amc
chown -R nadmin:amc $INSTALL_PATH

# Set appropriate permissions
chmod -R 750 $INSTALL_PATH

echo "Setup complete. You can now start the service with: sudo systemctl start translation-service"