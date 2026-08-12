"""
Especificação Executável (Executable SDD) via Pydantic.

Em vez de descrever os dados em texto livre, a especificação é um modelo
computável que valida tipos, limites e restrições em tempo de instanciação.
"""

from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


class MoneyAmount(BaseModel):
    """Especificação rígida de valor monetário."""
    amount: Decimal = Field(..., gt=Decimal("0.00"), description="O valor deve ser estritamente positivo.")

    @field_validator("amount")
    def check_two_decimal_places(cls, v: Decimal) -> Decimal:
        # Garante precisão financeira de no máximo 2 casas decimais
        if v.as_tuple().exponent < -2:
            raise ValueError("O valor não pode ter mais de 2 casas decimais.")
        return v


class TransferRequestSpec(BaseModel):
    """Contrato executável de uma requisição de transferência."""
    source_account_id: str = Field(..., min_length=3, description="Identificador da conta de origem")
    target_account_id: str = Field(..., min_length=3, description="Identificador da conta de destino")
    amount: MoneyAmount

    @field_validator("target_account_id")
    def accounts_must_be_distinct(cls, v: str, info) -> str:
        if "source_account_id" in info.data and v == info.data["source_account_id"]:
            raise ValueError("A conta de destino não pode ser igual à conta de origem.")
        return v


class AccountStateSpec(BaseModel):
    """Estado verificável de uma conta bancária."""
    account_id: str
    balance: Decimal = Field(..., ge=Decimal("0.00"), description="Saldo nunca pode ser negativo (sem cheque especial)")
