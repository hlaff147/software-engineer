"""
Continuous Evaluation Harness.

Este componente atua como o juiz automatizado (SDD Vivo).
Ele compila o código gerado pelo agente em tempo de execução, injeta casos de teste
e verifica rigorosamente se todas as invariantes e contratos foram respeitados.
"""

from decimal import Decimal
from typing import Dict, Any, Tuple


class EvaluationResult:
    def __init__(self, success: bool, feedback: str = "", score: float = 0.0):
        self.success = success
        self.feedback = feedback
        self.score = score


class ContinuousEvaluationHarness:
    def __init__(self, intent_contract: Dict[str, Any]):
        self.intent_contract = intent_contract

    def evaluate_generated_code(self, code_str: str) -> EvaluationResult:
        """
        Executa a suíte de avaliação sobre o código-fonte fornecido pelo agente.
        """
        namespace: Dict[str, Any] = {}

        # 1. Checagem de Compilação / Sintaxe
        try:
            exec(code_str, namespace)
        except Exception as e:
            return EvaluationResult(
                success=False,
                feedback=f"FALHA DE SINTAXE/COMPILAÇÃO: {type(e).__name__}: {str(e)}",
                score=0.0
            )

        # 2. Checagem da Assinatura
        if "process_transfer" not in namespace:
            return EvaluationResult(
                success=False,
                feedback="FALHA DE CONTRATO: Função `process_transfer` não encontrada no módulo gerado.",
                score=0.1
            )

        process_transfer = namespace["process_transfer"]

        # 3. Teste de Invariantes em Tempo de Execução
        try:
            # Caso 1: Transferência Normal bem-sucedida
            src_bal, tgt_bal, amt = Decimal("100.00"), Decimal("50.00"), Decimal("30.00")
            success, new_src, new_tgt = process_transfer(src_bal, tgt_bal, amt)
            
            # Valida Invariante 1: Conservação de Valor
            assert (src_bal + tgt_bal) == (new_src + new_tgt), (
                f"Violação da Invariante de Conservação de Valor! "
                f"Soma inicial: {src_bal + tgt_bal}, Soma final: {new_src + new_tgt}"
            )
            assert success is True, "Deveria ter retornado True para transferência válida."
            assert new_src == Decimal("70.00")
            assert new_tgt == Decimal("80.00")

            # Caso 2: Transferência com Saldo Insuficiente (A armadilha para o agente!)
            src_bal, tgt_bal, amt = Decimal("20.00"), Decimal("50.00"), Decimal("100.00")
            success, new_src, new_tgt = process_transfer(src_bal, tgt_bal, amt)

            # Valida Invariante 2: Não-negatividade de Saldos
            assert new_src >= Decimal("0.00"), (
                f"VIOLAÇÃO DA INVARIANTE NO_NEGATIVE_BALANCE! "
                f"O saldo da conta de origem ficou negativo ({new_src}). O agente não pode permitir saldos negativos!"
            )
            assert new_tgt >= Decimal("0.00"), f"Saldo de destino ficou negativo: {new_tgt}"

            # Valida Invariante 1 novamente no caso de recusa
            assert (src_bal + tgt_bal) == (new_src + new_tgt), "Conservação de valor violada na recusa."
            assert success is False, "Transferência com saldo insuficiente deveria ter sido recusada (retornar False)."

        except AssertionError as ae:
            return EvaluationResult(
                success=False,
                feedback=f"REJEITADO PELO HARNESS SDD - {str(ae)}",
                score=0.4
            )
        except Exception as ex:
            return EvaluationResult(
                success=False,
                feedback=f"ERRO DE EXECUÇÃO INESPERADO: {type(ex).__name__}: {str(ex)}",
                score=0.2
            )

        # Se passou em todas as invariantes e testes do harness
        return EvaluationResult(
            success=True,
            feedback="APROVADO PELO HARNESS SDD: Todas as invariantes, tipos e contratos foram preservados com sucesso!",
            score=1.0
        )
