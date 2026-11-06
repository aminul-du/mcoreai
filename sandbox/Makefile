# =============================================================================
# Makefile — standardized operations for the Fabric sandbox
# =============================================================================

.PHONY: help build up down logs ps health clean test lint security deploy

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build all images
	docker compose build

up: ## Start all services (dev)
	docker compose up -d --build

up-prod: ## Start all services (production overlay)
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

down: ## Stop all services
	docker compose down

logs: ## Tail logs
	docker compose logs -f

ps: ## Show service status
	docker compose ps

health: ## Check health of all services
	@for svc in web policy ingest neteng cyberrange shorborno; do \
		status=$$(docker inspect --format='{{.State.Health.Status}}' fabric-$$svc 2>/dev/null || echo "not-running"); \
		printf "  %-15s %s\n" "$$svc" "$$status"; \
	done

clean: ## Remove containers, volumes, images
	docker compose down -v --rmi local

test: ## Run all tests locally
	@echo "Running Python tests..."
	@for d in services/ingestion modules/neteng modules/cyberrange modules/shorborno; do \
		(cd $$d && python -m pytest tests/ -v) || true; \
	done

lint: ## Lint all services
	@echo "Linting Python..."
	@for d in services/ingestion modules/neteng modules/cyberrange modules/shorborno; do \
		(cd $$d && ruff check app/ --fix) || true; \
	done

security: ## Run Trivy scan on all Dockerfiles
	trivy config . --severity CRITICAL,HIGH

bake: ## Build all images with Buildx Bake (multi-arch)
	docker buildx bake -f docker-bake.hcl --print

deploy: ## Deploy via SSH to production host
	ssh $(DEPLOY_USER)@$(DEPLOY_HOST) "cd /opt/fabric-sandbox && git pull && make up-prod"
