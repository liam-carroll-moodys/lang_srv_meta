# Translation Service

This is a Flask-based translation service using the M2M100 model.

## Prerequisites

- Python 3.7+
- Git
- Root access (for installation and running)

## Installation

1. Clone the repository:
git clone https://your-repo-url.git translation-service
cd translation-service

2. Run the setup script as root:
sudo ./scripts/setup.sh

This script will install the service to `/nwsys/translation_srv/`, set up the Python virtual environment, install dependencies, and configure the systemd service to run as root.

## File Ownership and Permissions

After installation, all files and directories in `/nwsys/translation_srv/` will be owned by nadmin.

## Managing the Service

After installation, you can manage the service using systemctl:

- Start the service:
systemctl start translation-service

- Stop the service:
systemctl stop translation-service

- Restart the service:
systemctl restart translation-service

- Check the status of the service:
systemctl status translation-service

- Enable the service to start on boot:
systemctl enable translation-service

- Disable the service from starting on boot:
systemctl disable translation-service

## Viewing Logs

To view the logs of the service:
journalctl -u translation-service

## API Usage

Send a POST request to `http://localhost:5007/translate` with a JSON payload:

```json
{
  "text": "Hello, world!",
  "src_p": "en",
  "tgt_p": "fr"
}