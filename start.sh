#!/usr/bin/env bash
NAME=flask_app
docker build -t $NAME --build-arg NAME=$NAME .
#docker run -it -v $(pwd)/data:/opt/$NAME/data --env-file .env --rm $NAME "/bin/bash"
chmod +x entrypoint.sh
docker run -v $(pwd):/opt/$NAME -p 8000:5000 --env-file .env --rm $NAME
