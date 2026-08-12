# 🧮 Perda de Precisão em Números de Ponto Flutuante (IEEE 754)

> **Uma exploração teórico-prática sobre por que computadores erram contas decimais simples, o padrão IEEE 754, diferenças de paradigmas e como mitigar o *floating-point drift*.**

---

## 📌 Sumário

1. [O Problema: Por que $0.1 + 0.2 \neq 0.3$?](#-o-problema-por-que-01--02-%E2%89%A0-03)
2. [O Padrão IEEE 754 e a Representação Binária](#-o-padr%C3%A3o-ieee-754-e-a-representa%C3%A7%C3%A3o-bin%C3%A1ria)
3. [Acumulação de Erro (*Drift*) e Cancelamento Catastrófico](#-acumula%C3%A7%C3%A3o-de-erro-drift-e-cancelamento-catastr%C3%B3fico)
4. [Isso ocorre em todas as linguagens de programação?](#-isso-ocorre-em-todas-as-linguagens-de-programa%C3%A7%C3%A3o)
5. [Análise de Paradigmas: Máquina de Turing vs. Cálculo Lambda](#-an%C3%A1lise-de-paradigmas-m%C3%A1quina-de-turing-vs-c%C3%A1lculo-lambda)
6. [Como evitar o problema? (Soluções de Software)](#-como-evitar-o-problema-solu%C3%A7%C3%B5es-de-software)
7. [Experimentos Práticos & Como Executar](#-experimentos-pr%C3%A1ticos--como-executar)

---

## 🔍 O Problema: Por que $0.1 + 0.2 \neq 0.3$?

Na matemática de base 10 (decimal), estamos acostumados com frações exatas e dízimas periódicas:
- $1/2 = 0.5$ (finito)
- $1/3 = 0.333333...$ (dízima periódica infinita)

Um número decimal possui uma fração finita na base 10 se e somente se seus fatores primos no denominador forem compostos apenas por $2$ e $5$ (os fatores primos da base 10).

Nos computadores, a aritmética é realizada na **base 2 (binária)**, cujos únicos fatores primos são $2$.
Consequentemente:
- $1/2 = 0.1_2$ (finito)
- $1/4 = 0.01_2$ (finito)
- $1/10 = 0.1_{10} = 0.00011001100110011..._2$ (dízima periódica binária infinita!)
- $2/10 = 0.2_{10} = 0.0011001100110011..._2$ (dízima periódica binária infinita!)

Como o hardware possui memória finita (32 bits para `float` e 64 bits para `double`), a dízima binária precisa ser **truncada e arredondada**, introduzindo um minúsculo erro de aproximação logo na representação do número.

---

## ⚖️ O Padrão IEEE 754 e a Representação Binária

A maioria dos processadores modernos segue a especificação **IEEE 754** para aritmética de ponto flutuante.

No formato **Dupla Precisão (64 bits / `double`)**:

$$\text{Valor} = (-1)^{\text{sinal}} \times \left(1 + \sum_{i=1}^{52} b_{52-i} 2^{-i}\right) \times 2^{\text{expoente} - 1023}$$

| Componente | Bits | Descrição |
| :--- | :---: | :--- |
| **Sinal ($S$)** | 1 bit | `0` para positivo, `1` para negativo |
| **Expoente ($E$)** | 11 bits | Expoente com viés (*bias*) de 1023 |
| **Mantissa / Significando ($M$)** | 52 bits | A fração normalizada ($1.m_1m_2m_3...$) |

Quando tentamos armazenar $0.1$ em 64 bits IEEE 754:
O valor real armazenado é aproximadamente:
$$0.1000000000000000055511151231257827021181583404541015625$$

---

## 📈 Acumulação de Erro (*Drift*) e Cancelamento Catastrófico

Embora o erro de $0.00000000000000000555...$ pareça insignificante em uma única operação, ao realizar **milhões de iterações** (como em simulações científicas, cálculos financeiros ou engines de física), o erro se acumula progressivamente:

$$\text{Erro Acumulado} \approx N \times \epsilon$$

### Exemplo: Somar $0.0001$ exatamente $1.000.000$ de vezes
- **Resultado Matemático Esperado:** $100.0$
- **Resultado `float64` Real:** $99.99999999999042...$
- **Erro Acumulado:** $\approx 9.57 \times 10^{-12}$

---

## 🌐 Isso ocorre em todas as linguagens de programação?

### 1. No nível do Tipo Nativo (`float` / `double`)
**SIM, ocorre em absolutamente todas as linguagens.**
Quando uma linguagem (seja C, C++, Java, Python, Rust, Go, JavaScript ou Haskell) executa uma soma com o tipo flutuante nativo, ela instrui diretamente a **FPU (Floating-Point Unit)** do processador via instruções de assembly (como `ADDSS`, `ADDSD` no x86_64 ou `FADD` no ARM). Todas as linguagens obedecem ao mesmo silício e às mesmas especificações do IEEE 754.

### 2. Exemplos por Linguagem

| Linguagem | Tipo Nativo | Comportamento de $0.1 + 0.2$ |
| :--- | :--- | :--- |
| **Python** | `float` (64-bit IEEE 754) | `0.30000000000000004` |
| **JavaScript** | `Number` (64-bit IEEE 754) | `0.30000000000000004` |
| **Java** | `double` (64-bit IEEE 754) | `0.30000000000000004` |
| **C / C++** | `double` (64-bit IEEE 754) | `0.30000000000000004` |
| **Rust** | `f64` (64-bit IEEE 754) | `0.30000000000000004` |

---

## 🧠 Análise de Paradigmas: Máquina de Turing vs. Cálculo Lambda

Será que o paradigma da linguagem (Imperativo vs. Funcional vs. Orientado a Objetos) altera essa limitação?

**Não.** O paradigma não afeta a precisão dos números de ponto flutuante nativos.

* **Máquinas de Turing** e **Cálculo Lambda** são modelos matemáticos teóricos de computabilidade. Ambos assumem **fita/memória teoricamente infinita** e **precisão arbitrária**. Nenhum desses modelos impõe as limitações do IEEE 754.
* A limitação de ponto flutuante é de **engenharia física de hardware** (quantidade finita de transistores, registros e barramentos de 32/64 bits) e **eficiência computacional**, não de lógica matemática ou do modelo de computação escolhido.

---

## 🛡️ Como evitar o problema? (Soluções de Software)

Quando a precisão exata é exigida (ex: sistemas bancários, e-commerce, criptografia ou medições científicas), as linguagens oferecem abstrações de software:

### 1. Ponto Fixo Decimal / Arbitrary Precision
Armazenam os dígitos decimais como arrays de inteiros na memória e mantêm a escala explicitamente.
- **Python:** `decimal.Decimal`
- **Java:** `java.math.BigDecimal`
- **JavaScript:** `decimal.js` ou `bignumber.js`
- **C#:** `decimal`

### 2. Números Racionais / Frações Exatas
Representam números como a razão entre dois inteiros ($a/b$) de precisão arbitrária.
- **Python:** `fractions.Fraction`
- **Haskell:** `Data.Ratio` (`Rational`)
- **Ruby:** `Rational`

$$\frac{1}{3} + \frac{1}{6} = \frac{2}{6} + \frac{1}{6} = \frac{3}{6} = \frac{1}{2} \quad \text{(exatamente 0.5 sem perdas)}$$

### 3. Armazenamento em Inteiros (Unidade Mínima / Centavos)
Em vez de guardar $R\$ 10,50$ como `10.5` float, guarda-se `1050` inteiros representando **centavos**.
- É o padrão mais comum em APIs de pagamento (Stripe, PagSeguro, Mercado Pago).

---

## 🧪 Experimentos Práticos & Como Executar

### 1. Executando o Script Python Principal

O script [`floating_point_drift.py`](./floating_point_drift.py) executa 4 experimentos comparando `float`, `Decimal` e `Fraction`.

```bash
python3 floating-point-precision/floating_point_drift.py
```

### 2. Executando a Comparação em JavaScript

```bash
node floating-point-precision/comparisons/float_drift.js
```

### 3. Executando a Comparação em Java

```bash
javac floating-point-precision/comparisons/FloatDrift.java
java -cp floating-point-precision/comparisons FloatDrift
```
