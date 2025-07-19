# Vidays - Makefile

.PHONY: help install test test-unit test-integration test-coverage clean dev docker-build docker-up docker-down vite-dev vite-restart vite-exec vite-shell npm-install npm-build npm-test npm-deps docker-dev-full vite-logs dev-status

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
	docker build -t vidays-test . && docker run --rm -v $(pwd):/app -w /app vidays-test sh -c "PYTHONPATH=/app pytest -v"

test-unit: ## Run unit tests only
	PYTHONPATH=. pytest -m "not integration"

test-integration: ## Run integration tests only
	PYTHONPATH=. pytest -m integration

test-coverage: ## Run tests with coverage report
	PYTHONPATH=. pytest --cov=app --cov-report=html --cov-report=term-missing

test-coverage-docker: ## Run tests with coverage in Docker
	docker build -t vidays-test . && docker run --rm -v $(pwd):/app -w /app vidays-test sh -c "PYTHONPATH=/app pytest -v --cov=app --cov-report=html --cov-report=term-missing"

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
	docker-compose logs -f web

vite-logs: ## Show Vite development server logs only
	docker-compose logs -f web

flask-dev: ## Start Flask development server with auto-reload
	docker-compose exec web flask run --host=0.0.0.0 --port=5000 --debug

flask-shell: ## Access Flask shell for debugging
	docker-compose exec web flask shell

flask-restart: ## Restart Flask development server
	docker-compose restart web && sleep 2 && docker-compose logs --tail=10 web

dev-status: ## Check development services status
	@echo "Development services status:"
	@docker-compose ps
	@echo ""
	@echo "Access URLs:"
	@echo "Flask API: http://localhost:${WEB_API_PORT:-5000}"
	@echo "Vite Frontend: http://localhost:${VITE_PORT:-5173} (run 'make vite-dev' to start)"
	@echo "phpMyAdmin: http://localhost:${PHPMYADMIN_PORT:-8080}"
	@echo "MailHog: http://localhost:${MAILHOG_WEB_PORT:-8025}"

docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start Docker containers (production mode)
	docker-compose up -d

docker-dev: ## Start Docker containers (development mode)
	docker-compose --profile dev up -d

docker-dev-restart: ## Restart Docker containers (development mode)
	docker-compose --profile dev down
	docker-compose --profile dev up -d

docker-dev-down: ## Stop Docker containers (development mode)
	docker-compose --profile dev down

vite-dev: ## Start Vite development server in web container
	docker-compose exec web npm run dev

vite-build:  ## Start Vite development server in web container
	docker-compose exec web npm run build

vite-restart: ## Restart Vite dev server in web container
	docker-compose exec web pkill -f "vite" || true
	docker-compose exec web npm run dev &

vite-exec: ## Execute command in web container (usage: make vite-exec cmd="npm install")
	docker-compose exec web $(cmd)

vite-shell: ## Open shell in web container
	docker-compose exec web bash

npm-install: ## Install npm packages in web container
	docker-compose exec web npm install

npm-build: ## Build frontend for production in web container
	docker-compose exec web npm run build

npm-test: ## Run frontend tests in web container
	docker-compose exec web npm test

npm-deps: ## Show npm dependencies in web container
	docker-compose exec web npm list

docker-dev-full: ## Start Docker containers and ensure Vite is running
	docker-compose --profile dev up -d
	@echo "Waiting for services to start..."
	@sleep 3
	@echo "Development servers status:"
	@echo "Flask API: http://localhost:${WEB_API_PORT:-5000}"
	@echo "Vite Frontend: http://localhost:${VITE_PORT:-5173}"
	@docker-compose ps

docker-down: ## Stop Docker containers
	docker-compose down

docker-test: ## Run tests in Docker environment (SQLite)
	docker build -t vidays-test . && docker run --rm -v $(pwd):/app -w /app vidays-test sh -c "PYTHONPATH=/app pytest -v"

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
