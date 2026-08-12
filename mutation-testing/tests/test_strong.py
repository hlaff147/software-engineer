"""
Suíte de Testes Forte (Strong Test Suite).

Esta suíte atinge 100% de Cobertura de Linhas E faz ASSERTIONS RÍGIDAS em
valores exatos e CONDIÇÕES DE BORDA (off-by-one).
Ela MATA TODOS OS MUTANTES!
"""

import pytest
from discount_calculator import DiscountCalculator, OrderItem



def run_strong_tests_on(calc_class: type[DiscountCalculator] = DiscountCalculator):
    """Executa os testes fortes em qualquer classe derivada de DiscountCalculator."""
    calc = calc_class()

    # Teste 1: Teste Exacto de Borda VIP no valor exato de R$ 200.00
    # Valida ROR (subtotal >= 200 vs subtotal > 200)
    items_vip_boundary = [OrderItem(name="Notebook Case", price=200.0, quantity=1)]
    res1 = calc.calculate_final_total(items_vip_boundary, is_vip=True)
    assert res1["subtotal"] == 200.0
    assert res1["discount_rate"] == 0.20, f"Esperado 0.20 de desconto VIP para 200.00, obtido {res1['discount_rate']}"
    assert res1["discount_amount"] == 40.0
    assert res1["shipping"] == 0.0  # VIP tem frete grátis
    assert res1["final_total"] == 160.0  # (200 - 40) + 0

    # Teste 2: Validação de Aritmética e Taxa de Desconto padrão (10%)
    # Valida AOR e CR (subtotal > 100 -> 0.10)
    items_normal = [OrderItem(name="Teclado", price=150.0, quantity=1)]
    res2 = calc.calculate_final_total(items_normal, is_vip=False)
    assert res2["subtotal"] == 150.0
    assert res2["discount_rate"] == 0.10, f"Esperado 0.10 de desconto para 150.00, obtido {res2['discount_rate']}"
    assert res2["discount_amount"] == 15.0
    assert res2["shipping"] == 15.0  # Não VIP e < 300 paga 15 de frete
    # Testa se o desconto foi SUBTRAÍDO e não SOMADO: (150 - 15) + 15 = 150.0
    assert res2["final_total"] == 150.0

    # Teste 3: Validação de Frete Grátis por valor alto (>= 300) para Não-VIP
    # Valida LCR (is_vip or subtotal >= 300)
    items_high = [OrderItem(name="Monitor", price=300.0, quantity=1)]
    res3 = calc.calculate_final_total(items_high, is_vip=False)
    assert res3["shipping"] == 0.0, "Subtotal R$ 300.00 deve conceder frete grátis mesmo para Não-VIP"

    # Teste 4: Pedido Vazio
    with pytest.raises(ValueError):
        calc.calculate_final_total([])


def test_strong_suite_original():
    """Testa a classe original com a suíte forte (todos os testes passam!)."""
    run_strong_tests_on(DiscountCalculator)
