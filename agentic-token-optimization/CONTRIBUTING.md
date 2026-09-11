# 🤝 Diretrizes de Contribuição — Token Router

Agradecemos o interesse em contribuir com o projeto **Token Router**! Este projeto é voltado para arquiteturas de alta eficiência de contexto e redução de custos operacionais em agentes de codificação.

---

## 🏗️ Como Configurar o Ambiente de Desenvolvimento

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/agentic-token-optimization.git
   cd agentic-token-optimization
   ```

2. **Verifique os testes existentes**:
   ```bash
   make test
   ```

3. **Execute a demonstração**:
   ```bash
   make demo
   ```

---

## 📐 Padrões de Código e Arquitetura

- **Zero Dependências Obrigatórias**: O núcleo (`src/token_router/core/` e CLI básica) deve continuar utilizando apenas a biblioteca padrão do Python 3 (`dataclasses`, `os`, `sys`, `argparse`, `typing`).
- **Desacoplamento de Workers**: Novos workers de IA devem estender `BaseWorker` em `src/token_router/workers/base.py`.
- **Cobertura de Testes**: Qualquer nova funcionalidade ou parâmetro na CLI deve vir acompanhado de testes correspondentes em `tests/`.

---

## 🚀 Como Submeter um Pull Request

1. Crie uma branch para a sua feature (`git checkout -b feature/novo-worker-doc`).
2. Adicione seus testes unitários em `tests/`.
3. Garanta que `make test` passe sem falhas.
4. Abra o Pull Request com uma descrição clara do ganho de eficiência ou otimização proposta.
