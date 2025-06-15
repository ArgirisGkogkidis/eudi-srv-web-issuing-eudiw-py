#!/bin/bash

# Exit on error
set -e

# Function to display usage
usage() {
    echo "Usage: $0 [start|stop|restart|status]"
    echo "  start   - Start the Flask application"
    echo "  stop    - Stop the Flask application"
    echo "  restart - Restart the Flask application"
    echo "  status  - Check the status of the Flask application"
    exit 1
}

# Function to check if Flask is running
check_flask() {
    if pgrep -f "flask run" > /dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to start Flask
start_flask() {
    if check_flask; then
        echo "Flask application is already running"
        return
    fi

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

    # Run Flask without SSL (Nginx will handle SSL)
    echo "Starting Flask application in background..."
    nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &

    # Get the process ID
    FLASK_PID=$!
    echo "Flask application started with PID: $FLASK_PID"
    echo "You can check the logs with: tail -f flask.log"
    echo "To stop the application, use: ./run.sh stop"
}

# Function to stop Flask
stop_flask() {
    if ! check_flask; then
        echo "Flask application is not running"
        return
    fi

    echo "Stopping Flask application..."
    pkill -f "flask run"
    echo "Flask application stopped"
}

# Function to check status
status_flask() {
    if check_flask; then
        echo "Flask application is running"
        ps aux | grep "flask run" | grep -v grep
    else
        echo "Flask application is not running"
    fi
}

# Main script logic
case "$1" in
    start)
        start_flask
        ;;
    stop)
        stop_flask
        ;;
    restart)
        stop_flask
        sleep 2
        start_flask
        ;;
    status)
        status_flask
        ;;
    *)
        usage
        ;;
esac 