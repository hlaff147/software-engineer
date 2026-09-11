# 🤖 Cursor Agent Skills — Token Optimization & Model Routing

Este diretório contém a especificação de **Skills para o Cursor Agent**, projetadas para delegar tarefas de I/O massivo e geração de boilerplate para modelos workers, economizando tokens e preservando a capacidade atencional do agente principal.

---

## 📂 Catálogo de Skills

| Arquivo de Skill | Propósito | Padrão / Comportamento |
|:---|:---|:---|
| [`bulk-reader.md`](./bulk-reader.md) | Leitor de Contexto em Massa | Intercepta leituras grandes e invoca o utilitário de síntese em tópicos densos. |
| [`code-writer.md`](./code-writer.md) | Gerador de Boilerplate Direto em Disco | Gera testes e código padronizado gravando diretamente no sistema de arquivos. |

---

## ⚙️ Como Ativar no Cursor

Você pode utilizar estas skills no Cursor de três maneiras:

### Opção 1: Copiar para `.cursor/rules/` (Recomendado para o Workspace)
Copie os arquivos `.md` diretamente para a pasta de regras do seu projeto:

```bash
mkdir -p .cursor/rules
cp agentic-token-optimization/agent/*.md .cursor/rules/
```

Dessa forma, o Cursor indexa automaticamente as regras através do frontmatter YAML (`name`, `description`, `globs`) e sabe exatamente quando acionar o leitor ou o escritor.

### Opção 2: Referência Direta via Contexto (`@`)
No chat ou Composer do Cursor, mencione o arquivo da skill para carregar o contexto da regra sob demanda:
```text
@agent/bulk-reader.md preciso entender como os módulos de pagamento se comunicam
```

### Opção 3: Adicionar ao `.cursorrules` Raiz
Você pode incorporar o conteúdo das diretrizes no arquivo global `.cursorrules` do repositório para impor a restrição de tamanho de arquivo a todas as sessões.
