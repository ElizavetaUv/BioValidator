ENV_DEV_FILE=.env-dev


build-images:
	docker compose --env-file=$(ENV_DEV_FILE) build

pull-images:
	docker compose --env-file=$(ENV_DEV_FILE) pull

.down-compose:
	docker compose --env-file=$(ENV_DEV_FILE) down

.up-compose:
	docker compose --env-file=$(ENV_DEV_FILE) up -d

run-compose: .down-compose .up-compose
