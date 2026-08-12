"""
MUTANTE 1: ROR (Relational Operator Replacement)
Modifica 'subtotal >= 200.0' para 'subtotal > 200.0'.
Se o teste não verificar especificamente o valor exato R$ 200.00, o mutante SOBREVIVE.
"""

from discount_calculator import OrderItem, DiscountCalculator



class MutantBoundaryCalculator(DiscountCalculator):
    @staticmethod
    def calculate_discount_rate(subtotal: float, is_vip: bool) -> float:
        # MUTANTE INJETADO: '>=' foi alterado para '>'
        if is_vip and subtotal > 200.0:
            return 0.20
        elif subtotal > 100.0:
            return 0.10
        return 0.00
