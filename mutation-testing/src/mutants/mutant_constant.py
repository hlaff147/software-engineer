"""
MUTANTE 3: CR (Constant Replacement)
Modifica o desconto padrão de '0.10' para '0.15'.
Altera o percentual de desconto concedido.
"""

from discount_calculator import DiscountCalculator



class MutantConstantCalculator(DiscountCalculator):
    @staticmethod
    def calculate_discount_rate(subtotal: float, is_vip: bool) -> float:
        if is_vip and subtotal >= 200.0:
            return 0.20
        elif subtotal > 100.0:
            # MUTANTE INJETADO: 0.15 em vez de 0.10
            return 0.15
        return 0.00
