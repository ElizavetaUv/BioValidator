#!/bin/bash -u

ENV_FILE=${ENV_FILE:-.env-dev}
COMPOSE_FRONTEND_FILE=${COMPOSE_FRONTEND_FILE:-docker-compose.frontend.yml}
COMPOSE_BACKEND_FILE=${COMPOSE_BACKEND_FILE:-docker-compose.backend.yml}

docker compose --env-file=$ENV_FILE --file=$COMPOSE_FRONTEND_FILE --file=$COMPOSE_BACKEND_FILE down \
   && docker compose --env-file=$ENV_FILE --file=$COMPOSE_FRONTEND_FILE --file=$COMPOSE_BACKEND_FILE pull \
   && docker compose --env-file=$ENV_FILE --file=$COMPOSE_FRONTEND_FILE  --file=$COMPOSE_BACKEND_FILE up -d