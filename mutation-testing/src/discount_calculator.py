"""
Calculadora de Desconto e Frete de E-commerce.

Este é o módulo alvo sob teste. Ele contém regras de negócio reais com
condições de borda que serão alvo de mutações intencionais.
"""

from dataclasses import dataclass


@dataclass
class OrderItem:
    name: str
    price: float
    quantity: int


class DiscountCalculator:
    """Calcula descontos progressivos e taxa de frete para um pedido."""

    @staticmethod
    def calculate_subtotal(items: list[OrderItem]) -> float:
        """Calcula o valor total dos itens sem desconto."""
        total = 0.0
        for item in items:
            total += item.price * item.quantity
        return total

    @staticmethod
    def calculate_discount_rate(subtotal: float, is_vip: bool) -> float:
        """
        Regra de Desconto:
        - Se for cliente VIP e subtotal >= R$ 200.00: 20% de desconto (0.20)
        - Se subtotal > R$ 100.00: 10% de desconto (0.10)
        - Caso contrário: 0% de desconto (0.00)
        """
        if is_vip and subtotal >= 200.0:
            return 0.20
        elif subtotal > 100.0:
            return 0.10
        return 0.00

    @staticmethod
    def calculate_shipping(subtotal: float, is_vip: bool) -> float:
        """
        Regra de Frete:
        - Frete Grátis (0.0) se for cliente VIP OU subtotal >= R$ 300.00
        - Frete Fixo de R$ 15.00 caso contrário.
        """
        if is_vip or subtotal >= 300.0:
            return 0.0
        return 15.00

    def calculate_final_total(self, items: list[OrderItem], is_vip: bool = False) -> dict[str, float]:
        """Calcula o resumo financeiro do pedido."""
        if not items:
            raise ValueError("O pedido deve conter pelo menos um item.")

        subtotal = self.calculate_subtotal(items)
        discount_rate = self.calculate_discount_rate(subtotal, is_vip)
        discount_amount = subtotal * discount_rate
        shipping = self.calculate_shipping(subtotal, is_vip)

        final_total = (subtotal - discount_amount) + shipping

        return {
            "subtotal": round(subtotal, 2),
            "discount_rate": discount_rate,
            "discount_amount": round(discount_amount, 2),
            "shipping": round(shipping, 2),
            "final_total": round(final_total, 2)
        }
