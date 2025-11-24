# Makefile for DrinkLink

.PHONY: help setup up down logs clean migrate test lint lint-be lint-fe format format-be format-fe

help:
	@echo "DrinkLink - Available commands:"
	@echo "  make setup       - Initial setup (creates .env, starts containers, runs migrations)"
	@echo "  make up          - Start all containers"
	@echo "  make down        - Stop all containers"
	@echo "  make logs        - View logs"
	@echo "  make migrate     - Run database migrations"
	@echo "  make clean       - Stop containers and remove volumes"
	@echo "  make shell-be    - Open backend shell"
	@echo "  make shell-fe    - Open frontend shell"
	@echo "  make lint        - Run linting on backend and frontend"
	@echo "  make lint-be     - Run backend linting (ruff, black, isort)"
	@echo "  make lint-fe     - Run frontend linting (ESLint)"
	@echo "  make format      - Format code (backend and frontend)"
	@echo "  make format-be   - Format backend code"
	@echo "  make format-fe   - Format frontend code"

setup:
	@chmod +x setup.sh
	@./setup.sh

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

migrate:
	docker-compose exec backend alembic upgrade head

migrate-create:
	@read -p "Enter migration message: " msg; \
	docker-compose exec backend alembic revision --autogenerate -m "$$msg"

clean:
	docker-compose down -v
	rm -rf backend/__pycache__ backend/app/__pycache__

shell-be:
	docker-compose exec backend /bin/sh

shell-fe:
	docker-compose exec frontend /bin/sh

restart:
	docker-compose restart

rebuild:
	docker-compose up -d --build

# Linting commands
lint: lint-be lint-fe

lint-be:
	@echo "Running backend linting..."
	cd backend && ruff check .
	cd backend && black --check .
	cd backend && isort --check-only .

lint-fe:
	@echo "Running frontend linting..."
	cd frontend && npm run lint

# Formatting commands
format: format-be format-fe

format-be:
	@echo "Formatting backend code..."
	cd backend && black .
	cd backend && isort .

format-fe:
	@echo "Formatting frontend code..."
	cd frontend && npm run format
