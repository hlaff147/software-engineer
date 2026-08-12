"""
Implementação Clássica do Serviço de Transferência.

Nesta abordagem tradicional, o código é escrito manualmente a partir de uma
especificação em linguagem natural (Markdown). Não há verificações de
propriedade nem garantias automatizadas ligadas à especificação original.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Account:
    account_id: str
    balance: float


class ClassicTransferService:
    def __init__(self, accounts: Dict[str, Account]):
        self.accounts = accounts

    def execute_transfer(self, source_id: str, target_id: str, amount: float) -> bool:
        """
        Executa a transferência de saldo entre duas contas.
        
        Nota de fragilidade: Se um desenvolvedor alterar este código sem ler a spec
        (ex: esquecendo de validar valor negativo ou salvando estado inconsistente),
        não há um harness automático para impedir a regressão.
        """
        if source_id not in self.accounts or target_id not in self.accounts:
            raise ValueError("Conta de origem ou destino inválida.")

        if source_id == target_id:
            raise ValueError("Conta de origem e destino devem ser diferentes.")

        if amount <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")

        source = self.accounts[source_id]
        target = self.accounts[target_id]

        if source.balance < amount:
            raise ValueError("Saldo insuficiente na conta de origem.")

        # Realiza a movimentação
        source.balance -= amount
        target.balance += amount
        return True
