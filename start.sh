#!/usr/bin/env bash
case "$1" in
    develop)
        docker-compose -f docker-compose-develop.yml build && docker-compose -f docker-compose-develop.yml up
        ;;
    test)
        docker-compose -f docker-compose-test.yml build && docker-compose -f docker-compose-test.yml up
        ;;
    production)
        docker-compose -f docker-compose.yml build && docker-compose -f docker-compose.yml up
        ;;
    *)
        exec "$@"
esac
