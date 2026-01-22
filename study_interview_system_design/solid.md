# SOLID — Perguntas comuns (com gatilhos)

## S — Single Responsibility Principle (SRP)

**Pergunta:** O que é SRP?

**Resposta curta:** uma classe/módulo deve ter **um motivo principal para mudar**; separa responsabilidades e reduz acoplamento.

**Gatilhos:** coesão, “mudanças por atores diferentes”, classes pequenas, separar regras de negócio de IO.

**Como explicar com exemplo:**
- `PedidoService` não deveria montar PDF + mandar e-mail + persistir + calcular desconto tudo junto.

---

## O — Open/Closed Principle (OCP)

**Pergunta:** Como manter código aberto para extensão e fechado para modificação?

**Resposta curta:** você adiciona comportamento **criando novas implementações** em vez de editar o fluxo existente.

**Gatilhos:** interfaces, composição, Strategy, polimorfismo, `switch`/`if` por tipo como cheiro.

---

## L — Liskov Substitution Principle (LSP)

**Pergunta:** O que quebra LSP?

**Resposta curta:** quando uma subclasse não pode substituir a superclasse sem “surpresas” (pré-condições mais fortes ou pós-condições mais fracas).

**Gatilhos:** contrato, invariantes, “se eu tiver `List` e recebo `ArrayList`, nada pode mudar”, herança vs composição.

**Exemplo clássico:** `Square extends Rectangle` onde `setWidth`/`setHeight` quebram expectativas.

---

## I — Interface Segregation Principle (ISP)

**Pergunta:** Por que interfaces “gordas” são ruins?

**Resposta curta:** clientes não devem depender de métodos que não usam; prefira interfaces pequenas e específicas.

**Gatilhos:** “fatia por cliente”, evitar `interface Pagamento { pagar(); estornar(); cancelar(); ... }` gigante.

---

## D — Dependency Inversion Principle (DIP)

**Pergunta:** O que é DIP e como o Spring ajuda?

**Resposta curta:** módulos de alto nível não dependem de detalhes; ambos dependem de abstrações; Spring injeta dependências via IoC/DI.

**Gatilhos:** injeção por construtor, interfaces/ports, adapters, testes com mocks/fakes.

---

## Pergunta bônus: SOLID é “regra absoluta”?

**Resposta curta:** não; é um conjunto de heurísticas. Em código pequeno, simplificar pode ser melhor do que abstrair cedo.

**Gatilhos:** YAGNI, custo de abstração, complexidade acidental.
