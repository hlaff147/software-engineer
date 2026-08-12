"""
Invariantes Verificáveis de Negócio.

As invariantes são regras fundamentais que DEVEM ser preservadas antes e
depois de qualquer operação do sistema, independentemente de como o código
foi gerado ou implementado.
"""

from decimal import Decimal
from typing import Dict
from .transfer_spec import AccountStateSpec


def assert_conservation_of_money(
    initial_accounts: Dict[str, AccountStateSpec],
    final_accounts: Dict[str, AccountStateSpec]
) -> None:
    """
    Invariante 1: Conservação de Valor.
    A soma de todos os saldos no sistema antes da transferência DEVE ser exatamente
    igual à soma de todos os saldos após a transferência. NENHUM dinheiro pode sumir ou ser criado.
    """
    initial_total = sum(acc.balance for acc in initial_accounts.values())
    final_total = sum(acc.balance for acc in final_accounts.values())

    assert initial_total == final_total, (
        f"Violação da Invariante de Conservação de Valor! "
        f"Total Inicial: {initial_total}, Total Final: {final_total}"
    )


def assert_no_negative_balances(accounts: Dict[str, AccountStateSpec]) -> None:
    """
    Invariante 2: Não-negatividade de saldos.
    Nenhuma conta pode terminar com saldo negativo.
    """
    for acc_id, acc in accounts.items():
        assert acc.balance >= Decimal("0.00"), (
            f"Violação da Invariante de Saldo Não-Negativo na conta {acc_id}: {acc.balance}"
        )
