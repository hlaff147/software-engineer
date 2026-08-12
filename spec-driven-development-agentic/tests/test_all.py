"""
Suíte de Testes Geral do Projeto SDD Agêntico.
"""

from decimal import Decimal
import pytest
from src.classic_sdd.transfer_service import ClassicTransferService, Account
from src.executable_sdd.transfer_spec import TransferRequestSpec, MoneyAmount, AccountStateSpec
from src.executable_sdd.invariants import assert_conservation_of_money, assert_no_negative_balances
from src.agentic_sdd_harness.main_agentic_loop import run_agentic_sdd_demo
from src.agentic_sdd_harness.continuous_evaluator import ContinuousEvaluationHarness, EvaluationResult


def test_classic_transfer_success():
    accounts = {
        "ACC_1": Account(account_id="ACC_1", balance=100.0),
        "ACC_2": Account(account_id="ACC_2", balance=50.0),
    }
    service = ClassicTransferService(accounts)
    result = service.execute_transfer("ACC_1", "ACC_2", 30.0)
    assert result is True
    assert accounts["ACC_1"].balance == 70.0
    assert accounts["ACC_2"].balance == 80.0


def test_classic_transfer_insufficient_funds():
    accounts = {
        "ACC_1": Account(account_id="ACC_1", balance=10.0),
        "ACC_2": Account(account_id="ACC_2", balance=50.0),
    }
    service = ClassicTransferService(accounts)
    with pytest.raises(ValueError, match="Saldo insuficiente"):
        service.execute_transfer("ACC_1", "ACC_2", 30.0)


def test_executable_spec_pydantic_validation():
    # Deve rejeitar contas iguais
    with pytest.raises(ValueError):
        TransferRequestSpec(
            source_account_id="ACC_SAME",
            target_account_id="ACC_SAME",
            amount=MoneyAmount(amount=Decimal("10.00"))
        )

    # Deve rejeitar valor <= 0
    with pytest.raises(ValueError):
        MoneyAmount(amount=Decimal("0.00"))


def test_invariants_conservation_failure():
    initial = {"A": AccountStateSpec(account_id="A", balance=Decimal("100.00"))}
    tampered = {"A": AccountStateSpec(account_id="A", balance=Decimal("90.00"))}
    
    with pytest.raises(AssertionError, match="Conservação de Valor"):
        assert_conservation_of_money(initial, tampered)


def test_agentic_loop_integration():
    """Garante que a demonstração do loop agêntico roda e atinge sucesso."""
    success = run_agentic_sdd_demo(max_iterations=3)
    assert success is True
