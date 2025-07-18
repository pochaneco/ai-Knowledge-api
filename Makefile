# AI Knowledge API - Makefile

.PHONY: help install test test-unit test-integration test-coverage clean dev docker-build docker-up docker-down

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

test: ## Run all tests
	pytest

test-unit: ## Run unit tests only
	pytest -m "not integration"

test-integration: ## Run integration tests only
	pytest -m integration

test-coverage: ## Run tests with coverage report
	pytest --cov=app --cov-report=html --cov-report=term-missing

clean: ## Clean up cache and temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/

dev: ## Start development server
	./scripts/run_app.sh local

docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start Docker containers
	docker-compose up -d

docker-down: ## Stop Docker containers
	docker-compose down

docker-test: ## Run tests in Docker environment
	docker-compose exec web pytest

lint: ## Run code linting
	flake8 app/ tests/
	black --check app/ tests/

format: ## Format code
	black app/ tests/
	isort app/ tests/

init-db: ## Initialize database
	flask db upgrade

migrate: ## Create database migration
	flask db migrate -m "$(message)"

upgrade-db: ## Apply database migrations
	flask db upgrade
