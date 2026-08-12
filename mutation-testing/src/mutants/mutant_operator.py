"""
MUTANTE 2: AOR (Arithmetic Operator Replacement)
Modifica '(subtotal - discount_amount)' para '(subtotal + discount_amount)'.
Soma o desconto em vez de subtrair!
"""

from discount_calculator import OrderItem, DiscountCalculator



class MutantOperatorCalculator(DiscountCalculator):
    def calculate_final_total(self, items: list[OrderItem], is_vip: bool = False) -> dict[str, float]:
        if not items:
            raise ValueError("O pedido deve conter pelo menos um item.")

        subtotal = self.calculate_subtotal(items)
        discount_rate = self.calculate_discount_rate(subtotal, is_vip)
        discount_amount = subtotal * discount_rate
        shipping = self.calculate_shipping(subtotal, is_vip)

        # MUTANTE INJETADO: '+' em vez de '-' na aplicação do desconto
        final_total = (subtotal + discount_amount) + shipping

        return {
            "subtotal": round(subtotal, 2),
            "discount_rate": discount_rate,
            "discount_amount": round(discount_amount, 2),
            "shipping": round(shipping, 2),
            "final_total": round(final_total, 2)
        }
