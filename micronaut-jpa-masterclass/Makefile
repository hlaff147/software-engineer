SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

GRADLE := ./gradlew
DOCKER_COMPOSE := docker compose
APP_URL ?= http://localhost:8080

.PHONY: help build test run up down clean logs logs-db shell psql verify-jpa bench status workshop


help: ## Show this help message with all available targets
	@echo "=================================================================="
	@echo " 🚛 Micronaut Data JPA Masterclass — Developer Automation Makefile"
	@echo "=================================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'
	@echo ""

## ============================================================================
## Local Development (H2 In-Memory)
## ============================================================================

build: ## Compile project and run AOT processors (skip tests)
	$(GRADLE) build -x test --no-daemon

test: ## Execute complete JUnit 5 test suite (all 6 JPA pillars)
	$(GRADLE) test --no-daemon

run: ## Run application locally on H2 database (http://localhost:8080)
	$(GRADLE) run

## ============================================================================
## Container Orchestration (Docker Compose + PostgreSQL 16)
## ============================================================================

up: ## Build images and start PostgreSQL + App containers in background
	$(DOCKER_COMPOSE) up --build -d
	@echo "Waiting for services to become healthy..."
	@sleep 6
	@echo "Application available at $(APP_URL)"

down: ## Stop all running containers and remove networks
	$(DOCKER_COMPOSE) down

status: ## View status of running Docker Compose services
	$(DOCKER_COMPOSE) ps

logs: ## Tail live application logs (view formatted SQL queries and parameter bindings)
	$(DOCKER_COMPOSE) logs -f app

logs-db: ## Tail live PostgreSQL database logs
	$(DOCKER_COMPOSE) logs -f postgres

shell: ## Open interactive shell inside running application container
	$(DOCKER_COMPOSE) exec app /bin/sh

psql: ## Open interactive psql shell to PostgreSQL database
	$(DOCKER_COMPOSE) exec postgres psql -U fleet_admin -d fleet_management

clean: ## Complete cleanup: remove containers, volumes, networks, and build artifacts
	$(DOCKER_COMPOSE) down -v --remove-orphans 2>/dev/null || true
	$(GRADLE) clean --no-daemon 2>/dev/null || true
	@echo "Environment cleaned successfully."

## ============================================================================
## JPA Deep-Dive Workshop Diagnostics & Benchmarks
## ============================================================================

workshop: up verify-jpa bench ## 🚀 One-command end-to-end demo: start containers, run all diagnostics & benchmark
	@echo ""
	@echo "🎉 Workshop demo finished successfully!"
	@echo "👉 Run 'make logs' to inspect Hibernate SQL statements and bound parameters."
	@echo "👉 Run 'make down' when you want to stop the environment."
	@echo ""


verify-jpa: ## Run automated JPA diagnostic suite via REST API against running stack
	@echo "=================================================================="
	@echo " 🔬 RUNNING JPA DEEP-DIVE DIAGNOSTIC SUITE"
	@echo "=================================================================="
	@echo "─── [1/6] Seeding Workshop Test Dataset..."
	@curl -s -X POST $(APP_URL)/api/diagnostic/seed | python3 -m json.tool || curl -s -X POST $(APP_URL)/api/diagnostic/seed
	@echo ""
	@echo "─── [2/6] Verifying First-Level Cache (L1) Hit & Identity Guarantee..."
	@curl -s $(APP_URL)/api/diagnostic/l1-cache | python3 -m json.tool || curl -s $(APP_URL)/api/diagnostic/l1-cache
	@echo ""
	@echo "─── [3/6] Verifying Dirty Checking (Snapshot Comparison & Auto-UPDATE)..."
	@curl -s -X POST $(APP_URL)/api/diagnostic/dirty-checking | python3 -m json.tool || curl -s -X POST $(APP_URL)/api/diagnostic/dirty-checking
	@echo ""
	@echo "─── [4/6] Verifying Detached Entity Lifecycle & merge()..."
	@curl -s -X POST $(APP_URL)/api/diagnostic/detach-lifecycle | python3 -m json.tool || curl -s -X POST $(APP_URL)/api/diagnostic/detach-lifecycle
	@echo ""
	@echo "─── [5/6] Demonstrating N+1 Query Trap vs @BatchSize Mitigation..."
	@curl -s $(APP_URL)/api/diagnostic/n-plus-1 | python3 -m json.tool || curl -s $(APP_URL)/api/diagnostic/n-plus-1
	@echo ""
	@echo "─── [6/6] Simulating Optimistic Locking Conflict (@Version)..."
	@curl -s -X POST $(APP_URL)/api/diagnostic/optimistic-lock | python3 -m json.tool || curl -s -X POST $(APP_URL)/api/diagnostic/optimistic-lock
	@echo ""
	@echo "─── Hibernate Performance Statistics Summary:"
	@curl -s $(APP_URL)/api/diagnostic/statistics | python3 -m json.tool || curl -s $(APP_URL)/api/diagnostic/statistics
	@echo ""
	@echo "=================================================================="
	@echo " ✅ JPA DIAGNOSTIC SUITE COMPLETED"
	@echo "=================================================================="

bench: ## Execute bulk telemetry insertion benchmark (1,000 records with flush/clear)
	@echo "Running bulk ingestion benchmark (1000 records, batch_size=50)..."
	@curl -s -X POST "$(APP_URL)/api/telemetry/bulk-seed?total=1000&batchSize=50" | python3 -m json.tool || curl -s -X POST "$(APP_URL)/api/telemetry/bulk-seed?total=1000&batchSize=50"
