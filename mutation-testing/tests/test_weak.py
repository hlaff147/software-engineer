"""
Suíte de Testes Fraca (Weak Test Suite).

Esta suíte atinge 100% DE COBERTURA DE LINHAS (Line Coverage), pois chama
todas as funções com todos os caminhos de 'if'. No entanto, como faz apenas
assertions superficiais (ex: `assert result is not None`), ELA DEIXA OS MUTANTES SOBREVIVEREM!
"""

import pytest
from discount_calculator import DiscountCalculator, OrderItem



def run_weak_tests_on(calc_class: type[DiscountCalculator] = DiscountCalculator):
    """Executa os testes fracos em qualquer classe derivada de DiscountCalculator."""
    calc = calc_class()

    # Teste 1: Compra VIP alta (Executa branch VIP >= 200)
    items = [OrderItem(name="Item A", price=250.0, quantity=1)]
    res1 = calc.calculate_final_total(items, is_vip=True)
    # ASSERTION FRACA: Apenas verifica se o dicionário não é nulo e tem a chave final_total
    assert res1 is not None
    assert "final_total" in res1

    # Teste 2: Compra Normal > 100 (Executa branch subtotal > 100)
    items2 = [OrderItem(name="Item B", price=150.0, quantity=1)]
    res2 = calc.calculate_final_total(items2, is_vip=False)
    # ASSERTION FRACA: Apenas verifica se é dicionário
    assert isinstance(res2, dict)

    # Teste 3: Compra Pequena sem VIP (Executa branch subtotal <= 100)
    items3 = [OrderItem(name="Item C", price=50.0, quantity=1)]
    res3 = calc.calculate_final_total(items3, is_vip=False)
    assert res3["subtotal"] > 0

    # Teste 4: Pedido Vazio
    with pytest.raises(ValueError):
        calc.calculate_final_total([])


def test_weak_suite_original():
    """Testa a classe original com a suíte fraca (todos os testes passam!)."""
    run_weak_tests_on(DiscountCalculator)
