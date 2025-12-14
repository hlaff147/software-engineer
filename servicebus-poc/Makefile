# ============================================
# Makefile - Azure Service Bus PoC
# ============================================

.PHONY: help docker-up docker-down docker-logs app test test-light test-heavy clean k6-bad k6-good k6-all metrics-collect analyze

# Configurações
DOCKER_COMPOSE=docker-compose
MVN=./mvnw
STRESS_TEST=./stress-test.sh

# ============================================
# HELP
# ============================================
help:
	@echo ""
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║     Azure Service Bus PoC - Makefile                       ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Comandos disponíveis:"
	@echo ""
	@echo "  INFRAESTRUTURA:"
	@echo "    make docker-up      - Iniciar containers (SQL Edge + Service Bus Emulator)"
	@echo "    make docker-down    - Parar containers"
	@echo "    make docker-logs    - Ver logs do emulador"
	@echo ""
	@echo "  APLICAÇÃO:"
	@echo "    make app            - Compilar e rodar a aplicação Spring Boot"
	@echo "    make build          - Apenas compilar (sem rodar)"
	@echo ""
	@echo "  K6 LOAD TESTS:"
	@echo "    make k6-bad         - Load test no bad-producer (resource leak)"
	@echo "    make k6-good        - Load test no good-producer (best practice)"
	@echo "    make k6-all         - Executar ambos os testes em sequência"
	@echo ""
	@echo "  MÉTRICAS E ANÁLISE:"
	@echo "    make metrics-bad    - Coletar métricas JVM durante teste bad-producer"
	@echo "    make metrics-good   - Coletar métricas JVM durante teste good-producer"
	@echo "    make analyze        - Abrir Jupyter Notebook para análise"
	@echo ""
	@echo "  TESTES DE STRESS (bash):"
	@echo "    make test           - Teste padrão (100 mensagens)"
	@echo "    make test-light     - Teste leve (50 mensagens)"
	@echo "    make test-heavy     - Teste pesado (500 mensagens, 30 paralelos)"
	@echo ""
	@echo "  OUTROS:"
	@echo "    make clean          - Limpar artefatos de build"
	@echo "    make clean-results  - Limpar resultados de testes"
	@echo "    make all            - docker-up + aguardar + app (em foreground)"
	@echo ""

# ============================================
# DOCKER
# ============================================
docker-up:
	@echo "🐳 Iniciando containers..."
	$(DOCKER_COMPOSE) up -d
	@echo "⏳ Aguarde ~30s para o SQL Edge inicializar..."
	@echo "💡 Use 'make docker-logs' para acompanhar"

docker-down:
	@echo "🛑 Parando containers..."
	$(DOCKER_COMPOSE) down

docker-logs:
	$(DOCKER_COMPOSE) logs -f servicebus-emulator

docker-clean:
	@echo "🧹 Removendo containers e volumes..."
	$(DOCKER_COMPOSE) down -v

# ============================================
# APLICAÇÃO
# ============================================
build:
	@echo "🔨 Compilando aplicação..."
	$(MVN) clean package -DskipTests

app:
	@echo "🚀 Iniciando aplicação Spring Boot..."
	$(MVN) spring-boot:run

# ============================================
# TESTES DE STRESS (bash)
# ============================================
test:
	@echo "🧪 Executando teste padrão (100 mensagens)..."
	$(STRESS_TEST) 100 10

test-light:
	@echo "🧪 Executando teste leve (50 mensagens)..."
	$(STRESS_TEST) 50 5

test-heavy:
	@echo "🧪 Executando teste pesado (500 mensagens, 30 paralelos)..."
	$(STRESS_TEST) 500 30

# ============================================
# K6 LOAD TESTS
# ============================================
k6-install:
	@echo "📦 Verificando instalação do k6..."
	@which k6 > /dev/null || (echo "Instalando k6..." && brew install k6)

k6-bad:
	@echo "☠️ Executando k6 load test - BAD PRODUCER..."
	@mkdir -p analysis/results
	k6 run --out json=analysis/results/bad_producer_raw.json k6/bad-producer-test.js

k6-good:
	@echo "✅ Executando k6 load test - GOOD PRODUCER..."
	@mkdir -p analysis/results
	k6 run --out json=analysis/results/good_producer_raw.json k6/good-producer-test.js

k6-all: k6-bad
	@echo "⏳ Aguardando 10 segundos entre testes..."
	@sleep 10
	@$(MAKE) k6-good
	@echo "✅ Testes k6 completos! Resultados em analysis/results/"

# ============================================
# MÉTRICAS E ANÁLISE
# ============================================
metrics-install:
	@echo "📦 Instalando dependências Python..."
	pip install -r analysis/requirements.txt

metrics-collect:
	@echo "📊 Coletando métricas JVM por 120 segundos..."
	@mkdir -p analysis/results
	python analysis/metrics_collector.py --duration 120 --output analysis/results/jvm_metrics.csv

metrics-bad:
	@echo "📊 Coletando métricas durante teste bad-producer (120s)..."
	@mkdir -p analysis/results
	python analysis/metrics_collector.py --duration 120 --output analysis/results/bad_producer_jvm_metrics.csv

metrics-good:
	@echo "📊 Coletando métricas durante teste good-producer (120s)..."
	@mkdir -p analysis/results
	python analysis/metrics_collector.py --duration 120 --output analysis/results/good_producer_jvm_metrics.csv

analyze:
	@echo "📓 Abrindo Jupyter Notebook..."
	cd analysis && jupyter notebook load_test_analysis.ipynb

# ============================================
# OUTROS
# ============================================
clean:
	@echo "🧹 Limpando artefatos..."
	$(MVN) clean
	@rm -rf target/

clean-results:
	@echo "🧹 Limpando resultados de testes..."
	@rm -rf analysis/results/*.json analysis/results/*.csv analysis/results/*.png

all: docker-up
	@echo "⏳ Aguardando 35 segundos para infraestrutura inicializar..."
	@sleep 35
	@echo "🚀 Iniciando aplicação..."
	$(MVN) spring-boot:run

