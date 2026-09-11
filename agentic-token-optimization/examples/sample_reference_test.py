"""
Arquivo de Teste de Referência (Sample Reference Test).
Serve de padrão de estilo, asserções e estrutura para o worker 'code-writer'.
"""

import unittest
from examples.sample_large_service import PaymentGatewayService, Currency, TransactionStatus

class TestPaymentGatewayReference(unittest.TestCase):
    """Padrão canônico de testes de unidade do projeto."""

    def setUp(self):
        self.service = PaymentGatewayService()
        self.acc1 = self.service.register_account("111.222.333-44", initial_balance=50000, currency=Currency.BRL)
        self.acc2 = self.service.register_account("555.666.777-88", initial_balance=10000, currency=Currency.BRL)

    def test_successful_transfer(self):
        """Valida fluxo feliz de transferência."""
        tx = self.service.transfer_funds(
            source_id=self.acc1.account_id,
            dest_id=self.acc2.account_id,
            amount_cents=15000,
            idempotency_key="IDEMP-001"
        )
        self.assertEqual(tx.status, TransactionStatus.SETTLED)
        self.assertEqual(self.acc1.balance_cents, 35000)
        self.assertEqual(self.acc2.balance_cents, 25000)

    def test_insufficient_funds_declined(self):
        """Valida que saldo insuficiente resulta em transação DECLINED."""
        tx = self.service.transfer_funds(
            source_id=self.acc2.account_id,
            dest_id=self.acc1.account_id,
            amount_cents=999999,
            idempotency_key="IDEMP-002"
        )
        self.assertEqual(tx.status, TransactionStatus.DECLINED)

if __name__ == "__main__":
    unittest.main()
