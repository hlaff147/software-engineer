.PHONY: all test demo install clean help

help:
	@echo "Comandos disponíveis:"
	@echo "  make test      Executa a suíte de testes unitários (15 testes)"
	@echo "  make demo      Executa a demonstração interativa completa"
	@echo "  make install   Instala o pacote localmente em modo editável (pip install -e .)"
	@echo "  make legacy    Executa os testes dos scripts legados de compatibilidade"
	@echo "  make clean     Remove arquivos temporários e caches"

test:
	python3 -m unittest discover -s tests -p "test_*.py" -v

demo:
	bash examples/run_demo.sh

install:
	pip install -e .

legacy:
	bash scripts/test-token-router.sh

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build dist /tmp/router_err.log /tmp/GeneratedTransferTest.java
