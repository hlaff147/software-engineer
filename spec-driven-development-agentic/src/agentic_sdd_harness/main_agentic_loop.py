"""
Orquestrador do Loop Agêntico de SDD.

Demonstra como a Intenção Explícita e as Invariantes Verificáveis guiam um
Agente de IA até a entrega de um código perfeito e autêntico.
"""

import json
import os
from pathlib import Path
from .agent_generator import AgentCodeGenerator
from .continuous_evaluator import ContinuousEvaluationHarness


def run_agentic_sdd_demo(max_iterations: int = 3) -> bool:
    print("=" * 70)
    print("🤖 DEMONSTRAÇÃO DO SDD NA ERA AGÊNTICA (HARNESS & AGENTIC LOOP)")
    print("=" * 70)

    # 1. Carrega o Contrato de Intenção (SDD Vivo)
    contract_path = Path(__file__).parent / "intent_contract.json"
    with open(contract_path, "r", encoding="utf-8") as f:
        intent_contract = json.load(f)

    print(f"\n📋 [SDD ATIVO] Título da Spec: {intent_contract['spec_title']}")
    print(f"🎯 [INTENÇÃO] {intent_contract['explicit_intent']}")
    print("🛡️  [INVARIANTES OBRIGATÓRIAS]:")
    for inv in intent_contract["verifiable_invariants"]:
        print(f"   • {inv}")

    # 2. Inicializa o Agente e o Harness
    agent = AgentCodeGenerator(use_simulated_agent=True)
    harness = ContinuousEvaluationHarness(intent_contract)

    harness_feedback = None
    success = False

    for iteration in range(1, max_iterations + 1):
        print(f"\n----------------------------------------------------------------------")
        print(f"🔄 ITERAÇÃO {iteration}/{max_iterations}: Agente gerando/refinando código...")
        print(f"----------------------------------------------------------------------")

        # Agente gera código com base na spec + feedback anterior
        generated_code = agent.generate_code(intent_contract, harness_feedback)

        print("💻 Código Gerado pelo Agente:")
        print(generated_code)

        # Harness avalia o código gerado em relação às invariantes
        eval_result = harness.evaluate_generated_code(generated_code)

        if eval_result.success:
            print(f"\n✅ {eval_result.feedback}")
            print(f"🏆 Pontuação do Harness: {eval_result.score * 100:.0f}%")
            success = True
            break
        else:
            print(f"\n❌ {eval_result.feedback}")
            print("💬 Alimentando o Harness Feedback de volta para o Agente para Auto-Correção...")
            harness_feedback = eval_result.feedback

    print("\n" + "=" * 70)
    if success:
        print("🎉 CONCLUSÃO: O Agente convergiu para um código 100% aderente ao SDD Agêntico!")
    else:
        print("⚠️ CONCLUSÃO: O Agente não conseguiu satisfazer as invariantes no número limite de iterações.")
    print("=" * 70)

    return success


if __name__ == "__main__":
    run_agentic_sdd_demo()
