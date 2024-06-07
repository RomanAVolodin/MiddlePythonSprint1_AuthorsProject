.PHONY: help
help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -d | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build-gateway: ## Build gateway
	docker --log-level=debug build --progress=plain --pull --file=docker/nginx/Dockerfile --tag=rozarioagro/swarm-gateway:1.1 docker/nginx
	docker push rozarioagro/swarm-gateway:1.1

build-api: ## Build API
	docker --log-level=debug build --pull --file=docker/api/Dockerfile --tag=rozarioagro/swarm-django:1.1 .
	docker push rozarioagro/swarm-django:1.1

build-all: build-gateway build-api