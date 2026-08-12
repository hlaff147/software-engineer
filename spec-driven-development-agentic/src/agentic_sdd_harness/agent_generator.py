"""
Gerador de Código do Agente de IA.

Simula a geração de código por um Agente baseado em LLM.
Para demonstrar o loop do SDD Agêntico:
- Na tentativa 1 (Attempt 1), o Agente gera um código ingênuo/com bug (ex: não valida saldo insuficiente).
- Quando o Harness rejeita o código com um traceback de erro de invariante, o Agente analisa a falha e gera a versão corrigida (Attempt 2).
"""

import os
from typing import Dict, Any


class AgentCodeGenerator:
    def __init__(self, use_simulated_agent: bool = True):
        self.use_simulated_agent = use_simulated_agent
        self.attempts_counter = 0

    def generate_code(self, intent_contract: Dict[str, Any], harness_feedback: str | None = None) -> str:
        """
        Gera o código em Python com base no contrato de intenção e no feedback do Harness.
        """
        self.attempts_counter += 1

        if self.use_simulated_agent:
            return self._simulated_generation(harness_feedback)
        else:
            return self._llm_generation(intent_contract, harness_feedback)

    def _simulated_generation(self, harness_feedback: str | None) -> str:
        """
        Simulação determinística do comportamento de aprendizado de um agente agêntico.
        """
        if harness_feedback is None or self.attempts_counter == 1:
            # Tentativa 1: O agente gera código simples, mas ESQUECE de validar saldo insuficiente!
            # Isso causará saldo negativo, violando a invariante de NO_NEGATIVE_BALANCE.
            return '''from decimal import Decimal

def process_transfer(source_balance: Decimal, target_balance: Decimal, amount: Decimal) -> tuple[bool, Decimal, Decimal]:
    # Tentativa 1 (Simulada - Com Bug de Saldo Negativo)
    # Esqueceu de verificar se source_balance >= amount!
    new_source = source_balance - amount
    new_target = target_balance + amount
    return True, new_source, new_target
'''
        else:
            # Tentativa 2: O agente recebeu a reclamação do Harness e se auto-corrigiu!
            return '''from decimal import Decimal

def process_transfer(source_balance: Decimal, target_balance: Decimal, amount: Decimal) -> tuple[bool, Decimal, Decimal]:
    # Tentativa 2 (Auto-corrigida após feedback do Harness SDD)
    if amount <= Decimal("0.00"):
        return False, source_balance, target_balance

    if source_balance < amount:
        # Rejeita transferência por saldo insuficiente, mantendo integridade
        return False, source_balance, target_balance

    new_source = source_balance - amount
    new_target = target_balance + amount
    return True, new_source, new_target
'''

    def _llm_generation(self, intent_contract: Dict[str, Any], harness_feedback: str | None) -> str:
        """
        Estrutura pronta para integração com APIs reais de LLMs (OpenAI / Anthropic / Gemini).
        """
        prompt = f"Contrato de Intenção: {intent_contract}\n"
        if harness_feedback:
            prompt += f"O Harness de Validação rejeitou seu código anterior com o seguinte erro:\n{harness_feedback}\nPor favor, corrija o código mantendo as invariantes."

        # Retorna o modelo simulado como fallback caso não haja API key configurada no ambiente
        return self._simulated_generation(harness_feedback)
