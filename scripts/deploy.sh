#!/bin/bash -u

ENV_FILE=${ENV_FILE:-.env-dev}
COMPOSE_FILE=${COMPOSE_FILE:-docker-compose.frontend.yml}

docker compose --env-file=$ENV_FILE --file=$COMPOSE_FILE down \
   && docker compose --env-file=$ENV_FILE --file=$COMPOSE_FILE pull \
   && docker compose --env-file=$ENV_FILE --file=$COMPOSE_FILE up -d