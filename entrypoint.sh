#!/bin/bash

echo "Running python process"
echo -e "$EE_PRIVATE_KEY" | base64 -d > privatekey.pem
#exec gunicorn -w 2 main:app
exec python main.py