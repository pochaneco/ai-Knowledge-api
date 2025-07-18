# AI Knowledge API - Makefile

.PHONY: help install test test-unit test-integration test-coverage clean dev docker-build docker-up docker-down

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

test: ## Run all tests (local environment, fast)
	PYTHONPATH=. pytest

test-docker: ## Run tests in Docker environment (CI/CD)
	docker build -t ai-knowledge-test . && docker run --rm -v $(pwd):/app -w /app ai-knowledge-test sh -c "PYTHONPATH=/app pytest -v"

test-unit: ## Run unit tests only
	PYTHONPATH=. pytest -m "not integration"

test-integration: ## Run integration tests only
	PYTHONPATH=. pytest -m integration

test-coverage: ## Run tests with coverage report
	PYTHONPATH=. pytest --cov=app --cov-report=html --cov-report=term-missing

test-coverage-docker: ## Run tests with coverage in Docker
	docker build -t ai-knowledge-test . && docker run --rm -v $(pwd):/app -w /app ai-knowledge-test sh -c "PYTHONPATH=/app pytest -v --cov=app --cov-report=html --cov-report=term-missing"

clean: ## Clean up cache and temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/

dev: ## Start development server (local)
	./scripts/run_app.sh local

dev-docker: ## Start development server (Docker)
	docker-compose --profile dev up -d

dev-logs: ## Show development server logs (Docker)
	docker-compose logs -f web frontend

docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start Docker containers (production mode)
	docker-compose up -d

docker-dev: ## Start Docker containers (development mode)
	docker-compose --profile dev up -d

docker-down: ## Stop Docker containers
	docker-compose down

docker-test: ## Run tests in Docker environment (SQLite)
	docker build -t ai-knowledge-test . && docker run --rm -v $(pwd):/app -w /app ai-knowledge-test sh -c "PYTHONPATH=/app pytest -v"

docker-test-mysql: ## Run integration tests with MySQL
	docker-compose up -d db
	docker-compose --profile test run --rm test

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

status: ## Show Docker containers status
	docker-compose ps

logs: ## Show all Docker containers logs
	docker-compose logs -f

db-shell: ## Open database shell (Docker)
	docker-compose exec db mysql -u app_user -p ai_knowledge_db

setup-local: ## Setup local development environment
	pip install -r requirements.txt
	npm install
	./scripts/setup_env.sh local

setup-docker: ## Setup Docker development environment
	docker-compose build
	docker-compose --profile dev up -d
