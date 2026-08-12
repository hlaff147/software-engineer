# 02 - Operadores de Mutação (Mutation Operators)

## 1. O Que É um Operador de Mutação?

Um **Operador de Mutação** é uma regra predefinida que dita como o código-fonte original deve ser transformado para gerar um mutante. 

Ferramentas automáticas de mutation testing (como `mutmut` em Python, `Pitest` em Java ou `Stryker` em JavaScript/TypeScript) utilizam a árvore de sintaxe abstrata (AST - *Abstract Syntax Tree*) do código para aplicar esses operadores.

---

## 2. Principais Categorias de Operadores

### A. Operadores Relacionais (ROR - Relational Operator Replacement)
Substituem operadores de comparação por equivalentes vizinhos. São essenciais para capturar **erros de borda (off-by-one errors)**.

| Código Original | Mutante Gerado | Perigo se Sobreviver |
| :--- | :--- | :--- |
| `val > 100` | `val >= 100` | O valor exato `100` não está sendo testado |
| `val < 0` | `val <= 0` | O valor limite `0` não está coberto |
| `a == b` | `a != b` | Teste de igualdade ausente |

---

### B. Operadores Aritméticos (AOR - Arithmetic Operator Replacement)
Substituem operações matemáticas por outras operações.

| Código Original | Mutante Gerado | Perigo se Sobreviver |
| :--- | :--- | :--- |
| `total - desconto` | `total + desconto` | A fórmula financeira está incorreta |
| `subtotal * 0.10` | `subtotal / 0.10` | Cálculo de porcentagem invertido |
| `x % 2` | `x * 2` | Lógica de paridade quebrada |

---

### C. Operadores Lógicos e Condicionais (LOR / LCR)
Alteram a combinação de condições em declarações `if`, `while` e retornos booleanos.

| Código Original | Mutante Gerado | Perigo se Sobreviver |
| :--- | :--- | :--- |
| `is_vip and has_coupon` | `is_vip or has_coupon` | Regra de negócio combinada enfraquecida |
| `not is_active` | `is_active` | Negação invertida |
| `if status == "PAID":` | `if True:` | Curto-circuito que remove a verificação |

---

### D. Operadores de Substituição de Constantes (CR - Constant Replacement)
Modificam literais numéricos ou strings no código.

| Código Original | Mutante Gerado | Perigo se Sobreviver |
| :--- | :--- | :--- |
| `taxa = 0.05` | `taxa = 0.15` | Constante de imposto alterada sem percepção |
| `frete = 15.00` | `frete = 0.00` | Valor cobrado zerado |
| `return "SUCESSO"` | `return "ERRO"` | Mensagem de retorno alterada |

---

## 3. Tabela Comparativa de Exemplo

| Código Original | Mutante | Tipo de Operador | Resultado no Teste Fraco | Resultado no Teste Forte |
| :--- | :--- | :--- | :--- | :--- |
| `if valor > 100:` | `if valor >= 100:` | ROR | 🟢 **Passa (Sobrevive)** | 🔴 **Falha (Morto)** |
| `desconto = subtotal * 0.10` | `desconto = subtotal * 0.20` | CR | 🟢 **Passa (Sobrevive)** | 🔴 **Falha (Morto)** |
| `frete = 0.0 if valor >= 200 else 20.0` | `frete = 0.0 if valor > 200 else 20.0` | ROR | 🟢 **Passa (Sobrevive)** | 🔴 **Falha (Morto)** |
