# Especificação de Transferência Bancária (SDD Clássico - Estático)

**Versão:** 1.0.0 (Estática - Março/2026)  
**Autor:** Equipe de Arquitetura  
**Status:** Aprovado (porém desatualizado na prática)

---

## 1. Objetivo
Este documento especifica o comportamento do serviço de transferência entre duas contas bancárias.

## 2. Regras de Negócio (Texto)
1. A conta de origem deve ter saldo suficiente para realizar a transferência.
2. O valor da transferência deve ser obrigatoriamente maior que zero.
3. As contas de origem e destino devem ser válidas e distintas.
4. Após a transferência, o saldo da conta de origem deve ser debitado e o saldo da conta de destino deve ser creditado.
5. Em nenhuma hipótese a soma dos saldos das contas deve alterar como resultado da transferência (Princípio da Conservação de Valor).

## 3. Problema desta abordagem
Este documento é um arquivo Markdown legível por humanos. No entanto, ele não é executável nem compilável.
Se o código for alterado para permitir saldos negativos ou se o cálculo de taxas for introduzido sem atualizar este arquivo, ocorre o **Spec Drift**.
