"""
Property-Based Testing (PBT) como Especificação Executável.

Em vez de testar apenas cenários pontuais manuais, utilizamos o Hypothesis para
gerar milhares de combinações de dados e provar que as INVARIANTES de negócio
são matematicamente preservadas.
"""

from decimal import Decimal
from copy import deepcopy
from hypothesis import given, strategies as st
from .transfer_spec import AccountStateSpec, TransferRequestSpec, MoneyAmount
from .invariants import assert_conservation_of_money, assert_no_negative_balances


def execute_transfer_logic(
    accounts: dict[str, AccountStateSpec],
    request: TransferRequestSpec
) -> bool:
    """Função sob teste: realiza a transferência de acordo com o contrato executável."""
    src = accounts[request.source_account_id]
    tgt = accounts[request.target_account_id]

    if src.balance < request.amount.amount:
        # Transferência recusada por saldo insuficiente, saldos permanecem intactos
        return False

    src.balance -= request.amount.amount
    tgt.balance += request.amount.amount
    return True


@given(
    src_balance=st.decimals(min_value=Decimal("10.00"), max_value=Decimal("10000.00"), places=2),
    tgt_balance=st.decimals(min_value=Decimal("0.00"), max_value=Decimal("5000.00"), places=2),
    transfer_amount=st.decimals(min_value=Decimal("0.01"), max_value=Decimal("15000.00"), places=2)
)
def test_transfer_invariants_hypothesis(src_balance: Decimal, tgt_balance: Decimal, transfer_amount: Decimal):
    """
    Especificação de Propriedade:
    Para QUALQUER valor de saldo e QUALQUER valor de transferência:
    1. A conservação de valor deve ser mantida.
    2. Nenhum saldo pode ser negativo ao final.
    """
    initial_accounts = {
        "ACC_A": AccountStateSpec(account_id="ACC_A", balance=src_balance),
        "ACC_B": AccountStateSpec(account_id="ACC_B", balance=tgt_balance),
    }

    # Clona o estado antes da execução
    accounts_under_test = deepcopy(initial_accounts)

    try:
        req = TransferRequestSpec(
            source_account_id="ACC_A",
            target_account_id="ACC_B",
            amount=MoneyAmount(amount=transfer_amount)
        )
    except Exception:
        # Se os dados ferirem o contrato básico (Pydantic), a requisição é rejeitada na borda
        return

    # Executa a regra
    success = execute_transfer_logic(accounts_under_test, req)

    # VALIDAÇÃO DAS INVARIANTES DO HARNESS
    assert_conservation_of_money(initial_accounts, accounts_under_test)
    assert_no_negative_balances(accounts_under_test)

    if success:
        assert accounts_under_test["ACC_A"].balance == src_balance - transfer_amount
        assert accounts_under_test["ACC_B"].balance == tgt_balance + transfer_amount
    else:
        # Se falhou por saldo insuficiente, nada mudou
        assert accounts_under_test["ACC_A"].balance == src_balance
        assert accounts_under_test["ACC_B"].balance == tgt_balance
