#!/usr/bin/env bash
case "$1" in
    develop)
        docker-compose -f docker-compose-develop.yml build && docker-compose -f docker-compose-develop.yml up
        ;;
    test)
        echo "Test (not yet)"
        ;;
    production)
        docker-compose -f docker-compose.yml build && docker-compose -f docker-compose.yml up
        ;;
    *)
        exec "$@"
esac
