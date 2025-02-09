# BioValidator

Application for bioinformatic pipelines validation

### Deploying

Deploy application:

```bash
./scripts/deploy-all.sh
```

Build frontend/backend docker images:

```bash
ENV_FILE=.env-dev COMPOSE_FILE=docker-compose.{frontend/backend}.yml ./scripts/build.sh
```

Deploy frontend/backend with docker compose:

```bash
ENV_FILE=.env-dev COMPOSE_FILE=docker-compose.{frontend/backend}.yml ./scripts/deploy.sh
```

### Development

Lint backend:

```bash
ruff check backend/ scripts/
```

Format backend:

```bash
ruff check --fix --unsafe-fixes backend/ scripts/
```

Run backend tests (run it inside backend directory):

```bash
poetry run pytest tests/tests_unit
```
