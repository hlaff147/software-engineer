# Count Strings — Contagem de Strings por Expressão Regular

> **Categoria:** Teoria dos Autômatos · Programação Competitiva  
> **Linguagem:** Java 8  
> **Fonte:** [HackerRank — Count Strings](https://www.hackerrank.com/challenges/count-strings)

---

## 📋 Problema

Dada uma expressão regular customizada `R` sobre o alfabeto `{a, b}` e um inteiro `L`, contar quantas strings **distintas** de comprimento `L` são reconhecidas por `R`. Resposta módulo `10⁹ + 7`.

### Definição da Regex

| Forma | Significado |
|:---|:---|
| `a` ou `b` | Caractere literal |
| `(R₁R₂)` | Concatenação |
| `(R₁\|R₂)` | União (OR) |
| `(R₁*)` | Estrela de Kleene (0 ou mais repetições) |

### Restrições

- `1 ≤ T ≤ 50` (casos de teste)
- `1 ≤ |R| ≤ 100` (tamanho da regex)
- `1 ≤ L ≤ 10⁹` (comprimento alvo)

---

## 🧠 Abordagem — 4 Etapas

A solução transforma a expressão regular em um **DFA (Autômato Finito Determinístico)** e usa **exponenciação de matrizes** para contar caminhos de comprimento `L` em tempo `O(N³ log L)`.

```
Regex (string) → AST → NFA (Thompson) → DFA (Subconjuntos) → Matriz → M^L
```

### Etapa 1 — Parsing (Regex → AST)

Parser de **descida recursiva** que constrói uma **Árvore Sintática Abstrata (AST)** com nós:
- `CHAR_A`, `CHAR_B` — folhas
- `CONCAT(R1, R2)` — concatenação
- `UNION(R1, R2)` — união
- `STAR(R1)` — Kleene star

A gramática é não-ambígua: ao encontrar `(`, parseia `R1` e decide pelo próximo caractere (`|`, `*`, ou concatenação).

### Etapa 2 — Construção de Thompson (AST → NFA)

A **Construção de Thompson** converte cada nó da AST num fragmento de NFA com exatamente **um estado inicial** e **um estado de aceitação**, conectados por transições de caractere e transições-ε (epsilon).

Para `|R| ≤ 100`, o NFA resultante tem no máximo **~200 estados**.

### Etapa 3 — Construção de Subconjuntos (NFA → DFA)

**Por que não usar o NFA diretamente?** Em um NFA, uma mesma string pode ter múltiplos caminhos de aceitação (não-determinismo). Se contarmos caminhos ao invés de strings, o resultado será incorreto.

O DFA garante que **cada string tem exatamente um caminho**, eliminando duplicação.

**Algoritmo BFS:**
1. Estado DFA inicial = fecho-ε do estado inicial do NFA
2. Para cada estado DFA e cada caractere `{a, b}`, calcula o próximo conjunto de estados NFA + fecho-ε
3. Se o conjunto é novo, cria um novo estado DFA
4. Um estado DFA é de aceitação se contém o estado de aceitação do NFA

### Etapa 4 — Exponenciação de Matrizes (DFA → Contagem)

1. **Matriz de transição** `M[N×N]`: `M[i][j]` = número de caracteres que levam do estado `i` ao `j` (0, 1 ou 2)
2. **Calcula** `M^L` via exponenciação rápida em `O(N³ log L)`
3. **Resposta** = `Σ M^L[0][j]` para todo estado `j` de aceitação, módulo `10⁹ + 7`

---

## 📊 Complexidade

| Etapa | Tempo | Espaço |
|:---|:---|:---|
| Parsing | `O(\|R\|)` | `O(\|R\|)` |
| NFA (Thompson) | `O(\|R\|)` | `O(\|R\|)` |
| DFA (Subconjuntos) | `O(2^|R| · |R|)` worst-case | `O(2^|R|)` |
| Exponenciação | `O(N³ log L)` | `O(N²)` |

Na prática, `N` (estados do DFA) é muito menor que `2^|R|`.

---

## ▶️ Como Executar

```bash
cd java-developer/count-strings
javac Solution.java
echo "3
((ab)|(ba)) 2
((a|b)*) 5
((a*)(b(a*))) 100" | OUTPUT_PATH=/dev/stdout java Solution
```

**Saída esperada:**
```
2
32
100
```

---

## 🔍 Exemplos Explicados

| Regex | L | Linguagem | Contagem | Explicação |
|:---|:---|:---|:---|:---|
| `((ab)\|(ba))` | 2 | {"ab", "ba"} | **2** | Só "ab" e "ba" têm comprimento 2 |
| `((a\|b)*)` | 5 | Qualquer string de a's e b's | **32** | 2⁵ = 32 combinações possíveis |
| `((a*)(b(a*)))` | 100 | a\*ba\* (exatamente um 'b') | **100** | O 'b' pode estar em qualquer uma das 100 posições |
