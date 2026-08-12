"""
MUTANTE 4: LCR (Logical Connector Replacement)
Modifica 'if is_vip or subtotal >= 300.0' para 'if is_vip and subtotal >= 300.0'.
Exige que o cliente seja VIP E gaste R$ 300 para ter frete grátis.
"""

from discount_calculator import DiscountCalculator



class MutantLogicalCalculator(DiscountCalculator):
    @staticmethod
    def calculate_shipping(subtotal: float, is_vip: bool) -> float:
        # MUTANTE INJETADO: 'and' em vez de 'or'
        if is_vip and subtotal >= 300.0:
            return 0.0
        return 15.00
