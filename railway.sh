#!/bin/bash
# railway.sh

# Change to the project directory if needed
cd sportpost

# Run database migrations and collect static files before starting processes
python manage.py migrate && python manage.py collectstatic --noinput

# Start the worker process in the background
echo "Starting worker process..."
python manage.py runapscheduler &
worker_pid=$!

# Start the web process (e.g., using Gunicorn) in the background
echo "Starting web process..."
gunicorn sportpost.wsgi &
web_pid=$!

# Optional: Wait for both background processes
wait $worker_pid $web_pid
