#!/bin/bash
set -e

case "$1" in
    develop)
        echo "Running Development Server"
        echo -e "$EE_PRIVATE_KEY" | base64 -d > privatekey.pem
        exec python main.py
        ;;
    test)
        echo "Test (not yet)"
        ;;
    production)
        echo "Running Production Server"
        echo -e "$EE_PRIVATE_KEY" | base64 -d > privatekey.pem
        #exec gunicorn -w 2 main:app
        exec gunicorn -c gunicorn.py main:app
        ;;
    *)
        exec "$@"
esac