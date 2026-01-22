# Teorema CAP e a Escolha de Bancos de Dados

![CAP Theorem](./images/CAP.png)

O Teorema CAP afirma que um sistema distribuído pode garantir apenas duas das três propriedades ao mesmo tempo: Consistência, Disponibilidade e Tolerância a Partição.

## As Propriedades

- **Consistency (Consistência):** Todos os nós veem os mesmos dados ao mesmo tempo.
- **Availability (Disponibilidade):** Toda requisição recebe uma resposta (sucesso ou falha), sem garantia de que contém a escrita mais recente.
- **Partition Tolerance (Tolerância a Partições):** O sistema continua a operar apesar de quebras na comunicação entre os nós.

## Posicionamento no Diagrama

### 1. MongoDB (CP - Consistência e Tolerância a Partição)
- **Padrão:** O MongoDB, em sua configuração padrão (com Replica Sets), prioriza a Consistência. Se houver uma partição de rede e o nó primário ficar isolado, o sistema interrompe as escritas até que um novo primário seja eleito, garantindo que os dados não divirjam.

### 2. PostgreSQL (CA - Consistência e Disponibilidade)
- **Tende a:** Como um banco de dados relacional clássico, o Postgres foca em ACID. Em um cenário de nó único ou replicação síncrona simples, ele garante que os dados estejam consistentes e disponíveis. No entanto, ele tem dificuldades inerentes com a "Tolerância a Partição" em escalas globais distribuídas sem ferramentas adicionais.

### 3. Redis (AP - Disponibilidade e Tolerância a Partição)
- **Geralmente:** O Redis (especialmente em modo Cluster ou Sentinel) foca em baixíssima latência e alta disponibilidade. Em caso de partição, ele prefere continuar servindo dados (mesmo que potencialmente obsoletos) para manter a disponibilidade, sacrificando a consistência forte em favor da performance.

## Conclusão
A escolha do banco de dados depende do que o seu negócio não pode perder:
- Se você não pode perder dinheiro/transações: **Consistência (CP/CA)**.
- Se o seu sistema não pode ficar fora do ar por nada: **Disponibilidade (AP)**.
