---
name: code-writer
description: "Gera código padronizado (testes unitários, DTOs, configurações, scaffolding) a partir de arquivos de referência e especificações, gravando o resultado diretamente em disco sem saturar o contexto do Cursor."
globs: "**/*"
alwaysApply: false
---

# ✍️ Cursor Skill: Code Writer (Gerador de Boilerplate Direto em Disco)

Esta skill instrui o agente do **Cursor** sobre como delegar a geração de código repetitivo, arquivos de teste e scaffolding para um worker secundário, gravando o arquivo gerado **diretamente no sistema de arquivos** sem carregar o código na janela de contexto da sessão principal.

---

## 🎯 Quando Ativar Esta Skill

Ative e utilize esta skill automaticamente quando:
1. **O usuário pedir para gerar testes unitários** para uma classe ou serviço já existente (ex: *"Crie testes de unidade para o OrderService seguindo o padrão de UserServiceTest"*).
2. **Criação de DTOs, mappers ou entidades** que repetem a estrutura e convenções de arquivos já existentes no projeto.
3. **Scaffolding de configurações**: criação de stubs de Docker Compose, arquivos de migração SQL ou manifests de infraestrutura.

> [!IMPORTANT]
> **Regra de Ouro**: O código gerado NÃO deve ser devolvido como texto na resposta do chat se você puder gravá-lo diretamente no disco. Gerar centenas de linhas de código previsível em modelos de fronteira queima tokens de saída de alto custo.

---

## 🛠️ Como Executar a Delegação

O Cursor deve executar o utilitário `code-write.py` via terminal especificando a especificação funcional, o arquivo de referência de estilo e o arquivo alvo:

```bash
python3 agentic-token-optimization/scripts/code-write.py \
  --spec "<descrição exata do que deve ser implementado>" \
  --reference <caminho_do_arquivo_de_exemplo_existente> \
  --target <caminho_do_novo_arquivo_a_ser_criado>
```

### Exemplo Prático de Invocação:

```bash
# Gerando testes de integração espelhando outro teste existente
python3 agentic-token-optimization/scripts/code-write.py \
  --spec "Criar testes de integração para PaymentService cobrindo cenários de saldo insuficiente e timeout" \
  --reference src/test/java/com/service/AccountServiceTest.java \
  --target src/test/java/com/service/PaymentServiceTest.java
```

---

## 📋 Regras de Confiabilidade e Estilo

1. **Arquivo de Referência Obrigatório**: Sempre forneça um arquivo de referência `--reference`. Sem ele, o worker gerará código genérico desalinhado com os padrões do projeto (nomenclaturas, asserções, frameworks de mock).
2. **Contrato "Output Only Code"**: O worker gera exclusivamente o código fonte executável, sem blocos de formatação markdown (```) e sem explicações no corpo do arquivo.
3. **Pós-Verificação via Execução de Testes**:
   - Após a gravação em disco pelo script, o Cursor **NÃO** precisa ler o arquivo gerado inteiro.
   - Em vez disso, o Cursor deve rodar a suíte de testes do projeto (ex: `mvn test`, `pytest`, etc.).
   - Se ocorrer falha de compilação ou asserção, o Cursor lê pontualmente apenas as linhas do erro reportado no stack trace.
