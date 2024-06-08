.PHONY: help
help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -d | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build-gateway
build-gateway: ## Build gateway
	docker --log-level=debug build --progress=plain --pull --file=docker/nginx/Dockerfile --tag=rozarioagro/swarm-gateway:1.1 docker/nginx
	docker push rozarioagro/swarm-gateway:1.1

.PHONY: build-api
build-api: ## Build API
	docker --log-level=debug build --pull --file=docker/api/Dockerfile --tag=rozarioagro/swarm-django:1.1 .
	docker push rozarioagro/swarm-django:1.1

.PHONY: dump_database
dump_database: ## Dump current DB
	docker exec -t theatre-db pg_dumpall -c -U postgres > database_dump.sql

.PHONY: copy_to_remote
copy_to_remote: ## Copy files to remote server
	scp .env database_dump.sql docker-compose.yaml admin@84.201.177.111:~

build-all: build-gateway build-api