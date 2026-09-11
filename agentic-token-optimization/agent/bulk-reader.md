---
name: bulk-reader
description: "Delega a leitura e análise de múltiplos arquivos longos para um worker leve, sintetizando o conteúdo em tópicos densos sem inflar a janela de contexto do Cursor."
globs: "**/*"
alwaysApply: false
---

# 📖 Cursor Skill: Bulk Reader (Leitor de Contexto em Massa)

Esta skill define as diretrizes e procedimentos para o agente do **Cursor** delegar operações pesadas de I/O e leitura de arquivos para um modelo worker secundário leve, preservando a janela de contexto principal para raciocínio crítico.

---

## 🎯 Quando Ativar Esta Skill

Ative e utilize esta skill automaticamente quando:
1. **O usuário fizer perguntas que exigem inspecionar múltiplos arquivos** (ex: *"Como funciona o fluxo de autenticação entre o Controller, Service e Filter?"*).
2. **Qualquer arquivo alvo tiver mais de 350 linhas de código**.
3. **Varredura exploratória**: mapeamento de dependências, busca de anotações ou listagem de métodos sem necessidade de edição imediata.

> [!IMPORTANT]
> **Regra de Ouro**: NUNCA execute leituras completas de arquivos grandes diretamente usando ferramentas nativas de leitura se você apenas precisa entender a lógica ou responder a dúvidas conceituais. Use esta delegação.

---

## 🛠️ Como Executar a Delegação

O Cursor deve executar o utilitário `bulk-read.py` via terminal:

```bash
python3 agentic-token-optimization/scripts/bulk-read.py \
  --question "<pergunta clara e objetiva do que você precisa descobrir>" \
  --paths <caminho_arquivo_1> <caminho_arquivo_2> ...
```

### Exemplo Prático de Invocação:

```bash
# Investigando contratos de pagamento entre arquivos
python3 agentic-token-optimization/scripts/bulk-read.py \
  --question "Quais métodos manipulam persistência de dados e quais exceções são lançadas?" \
  --paths src/main/java/com/service/PaymentService.java src/main/java/com/service/AccountService.java
```

---

## 📋 Contrato de Saída Esperado do Worker

Ao processar a síntese gerada pelo worker, o Cursor deve incorporar as seguintes restrições:
- **Tópicos crus e densos**: cada tópico deve iniciar apontando diretamente o nome da classe, método ou linha de interesse.
- **Zero prolixidade**: rejeitar ou ignorar qualquer saudação, preâmbulo ("*Com certeza, analisei os arquivos...*") ou consideração genérica.
- **Foco estrito**: conter apenas respostas aos pontos levantados na `--question`.

---

## ⚡ Exceção: Leituras Pontuais Direcionadas (Targeted Reads)

Se após a síntese do `bulk-reader` você identificar que precisa **editar** um trecho específico de código:
- **NÃO leia o arquivo inteiro**.
- Utilize a ferramenta nativa de leitura com parâmetros de recorte (`offset`/`limit` ou `StartLine` e `EndLine`) cobrindo apenas as linhas onde a modificação será realizada.
