# CAP, ACID e Locks: Conceitos Essenciais de Dados

Este guia resume os pilares de consistência, transações e concorrência em sistemas distribuídos e bancos de dados.

---

## 1. Teorema CAP (Sistemas Distribuídos)
Afirma que em um sistema distribuído, você só pode garantir **2 de 3** propriedades simultaneamente em caso de falha de rede.

- **C (Consistency - Consistência):** Todos os nós veem o mesmo dado ao mesmo tempo (leitura forte).
- **A (Availability - Disponibilidade):** Toda requisição recebe uma resposta (mesmo que com dado antigo), sem erro.
- **P (Partition Tolerance - Tolerância a Partição):** O sistema continua funcionando mesmo se a comunicação entre os nós cair.

### Combinações:
- **CP (Consistência + Partição):** Se houver falha de rede, o sistema para de responder para não entregar dados inconsistentes (Ex: MongoDB em modo padrão, HBase).
- **AP (Disponibilidade + Partição):** Se houver falha, o sistema continua respondendo, mas pode entregar dados desatualizados (Ex: Cassandra, DynamoDB, Redis Cluster).
- **CA (Consistência + Disponibilidade):** Difícil de garantir em sistemas distribuídos, pois assume que a rede nunca falha. Geralmente bancos relacionais tradicionais (Postgres, MySQL) em configuração não-distribuída ou com replicação síncrona rígida.

---

## 2. ACID (Transações em Bancos de Dados)
Conjunto de propriedades que garantem a confiabilidade de transações em bancos de dados (ex: SQL).

- **A (Atomicidade):** "Tudo ou nada". Se uma parte da transação falha, toda a transação é revertida (Rollback).
- **C (Consistência):** Garante que o banco saia de um estado válido para outro estado válido, respeitando regras de integridade (FKs, Constraints).
- **I (Isolamento):** Define como e quando as alterações feitas por uma operação tornam-se visíveis para as outras. Evita leituras sujas ou fantasmas.
- **D (Durability - Durabilidade):** Garante que, uma vez confirmado (Commit), o dado permanecerá gravado mesmo em falhas de sistema ou energia.

---

## 3. LOCKS (Controle de Concorrência)
Mecanismos para gerenciar acessos simultâneos ao mesmo recurso e evitar **Race Conditions**.

### Lock Otimista (Optimistic Lock)
- **Como funciona:** Não bloqueia o recurso. Assume-se que conflitos são raros. Cada registro tem uma coluna `version`. Ao gravar, o banco verifica se a versão ainda é a mesma do momento da leitura.
- **Trade-off:** Mais performance (sem filas), mas gera exceções que a aplicação deve tratar (retry).
- **Exemplo:** `UPDATE account SET balance = 50, version = 2 WHERE id = 123 AND version = 1;`

### Lock Pessimista (Pessimistic Lock)
- **Como funciona:** Bloqueia o recurso no momento da leitura (`SELECT FOR UPDATE`). Ninguém mais pode ler ou escrever naquele registro até que a transação termine.
- **Trade-off:** Garante integridade total em cenários de alta disputa, mas pode causar gargalos de performance e Deadlocks.
- **Exemplo:** Um sistema financeiro debitando saldo de uma carteira.

### Lock Distribuído
- **Como funciona:** Quando o recurso não está em um único banco, mas distribuído entre microserviços. Usa-se ferramentas como **Redis** (Redlock) ou **Zookeeper** para criar uma "chave" global de trava.
- **Uso Comum:** Evitar que dois processos diferentes enviem o mesmo e-mail ou processem o mesmo arquivo simultaneamente.
