#!/usr/bin/env bash
echo -e "$EE_PRIVATE_KEY" | base64 -d > privatekey.pem
python main.py
