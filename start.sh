#!/bin/bash

# Exit on error
set -e

# Check for virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Error: Virtual environment (venv) not found!"
    echo "Please follow the setup process to create and configure your virtual environment first."
    exit 1
fi

# Check if Flask is installed
if ! command -v flask &> /dev/null; then
    echo "Error: Flask not found in virtual environment!"
    echo "Please ensure all required packages are installed in your virtual environment."
    exit 1
fi

# Set Flask environment variables
export FLASK_APP=app
export FLASK_ENV=production
export FLASK_DEBUG=0

# Run Flask with SSL in background
echo "Starting Flask application in background..."
# nohup flask run --host=0.0.0.0 --port=5000 --cert=/etc/eudiw/pid-issuer/cert/cert.pem --key=/etc/eudiw/pid-issuer/cert/key.pem > flask.log 2>&1 &
nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &

# Get the process ID
FLASK_PID=$!
echo "Flask application started with PID: $FLASK_PID"
echo "You can check the logs with: tail -f flask.log"
echo "To stop the application, use: kill $FLASK_PID" 
