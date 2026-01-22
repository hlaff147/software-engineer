# Padrão Saga: Orquestração e Transações de Compensação

![Saga Pattern Sequence](./images/Saga2-2025-12-27-235823.png)

Este diagrama de sequência detalha como o sistema lida com falhas em transações distribuídas que abrangem múltiplos microserviços, utilizando o padrão Saga Orquestrada.

## Padrões e Técnicas Utilizadas

- **Saga Orchestration:** Um componente central (Order Orchestrator) coordena as etapas e decide o que fazer em caso de erro.
- **Compensating Transaction (Transação de Compensação):** Como não há "rollback" automático em bancos de dados distribuídos, o sistema executa uma ação inversa (ex: devolver o item ao estoque) para desfazer uma alteração anterior.
- **Stateful Management:** O pedido transita entre estados (`PENDING` -> `CANCELLED` ou `COMPLETED`) conforme as respostas dos serviços.

## O Fluxo (Happy Path até a Falha)

1. **Início:** O cliente envia um `POST /checkout`. O orquestrador cria o pedido como `PENDING`.
2. **Reserva de Estoque:** O orquestrador envia o comando para o **Stock Service**. O estoque é decrementado com sucesso.
3. **Pagamento:** O orquestrador envia o comando de cobrança para o **Payment Service**.
4. **O Erro:** O processamento falha por "Saldo Insuficiente".

## O Fluxo de Compensação (Rollback Lógico)

Diferente de uma transação SQL local, o item já foi decrementado no banco de dados do estoque. Precisamos "voltar atrás" de forma lógica:

1. O orquestrador detecta a falha de pagamento.
2. **Comando de Compensação:** O orquestrador envia um comando específico para o **Stock Service** para **LIBERAR ESTOQUE**.
3. O Stock Service incrementa o banco de dados (devolução do item).
4. O orquestrador atualiza o pedido final para o estado `CANCELLED`.
5. O cliente recebe a mensagem de erro amigável.

## Conclusão
O padrão Saga garante a **Consistência Eventual**. Embora haja um momento em que o estoque está reservado e o pagamento ainda não ocorreu, o sistema garante que, ao final, ou tudo deu certo ou todas as alterações foram desfeitas.
