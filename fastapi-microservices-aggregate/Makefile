SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

DOCKER_COMPOSE ?= docker compose
PYTHON ?= .venv/bin/python3
PYTEST ?= .venv/bin/pytest
RUFF ?= .venv/bin/ruff
UV ?= uv

.PHONY: help install up down ps logs test lint format demo clean

help: ## Show this help message with available commands
	@echo "=================================================================="
	@echo " 🚀 FastAPI Microservices Aggregate Laboratory (Gateway + DDD)    "
	@echo "=================================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'
	@echo ""

install: ## Setup Python virtualenv and install all dependencies
	$(UV) sync --extra dev || $(PYTHON) -m pip install -e ".[dev]"

up: ## Build and start all 6 containers in the background
	$(DOCKER_COMPOSE) up --build -d
	@echo "Services booting up... Gateway will be available at http://localhost:8000"

down: ## Stop all running containers and remove networks
	$(DOCKER_COMPOSE) down

ps: ## View status of all Docker Compose containers
	$(DOCKER_COMPOSE) ps

logs: ## Tail aggregated logs from all services
	$(DOCKER_COMPOSE) logs -f

logs-gateway: ## Tail logs for gateway-aggregator
	$(DOCKER_COMPOSE) logs -f gateway-aggregator

logs-order: ## Tail logs for order-service
	$(DOCKER_COMPOSE) logs -f order-service

test: ## Run complete test suite (unit, integration, contracts)
	$(PYTEST) -v

lint: ## Run Ruff linter
	$(RUFF) check .

format: ## Run Ruff formatter check
	$(RUFF) format --check .

format-fix: ## Auto-format code using Ruff
	$(RUFF) format .

demo: ## Run the interactive didactic showcase script
	$(PYTHON) scripts/demo_showcase.py

clean: ## Clean Python cache and build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
