#!/usr/bin/env python3
"""
Walkthrough Interativo: A Transição do SDD Clássico para o SDD Agêntico.

Este script executa sequencialmente os 3 modelos de SDD demonstrados no repositório:
1. SDD Clássico (Documento de texto estático + Implementação manual)
2. SDD Executável (Pydantic + Invariantes de Negócio + Property-Based Testing com Hypothesis)
3. SDD Agêntico no Harness (Intenção Máquina + Agente Autônomo + Auto-correction Feedback Loop)
"""

import sys
from decimal import Decimal
from src.classic_sdd.transfer_service import ClassicTransferService, Account
from src.executable_sdd.transfer_spec import TransferRequestSpec, MoneyAmount, AccountStateSpec
from src.executable_sdd.invariants import assert_conservation_of_money, assert_no_negative_balances
from src.agentic_sdd_harness.main_agentic_loop import run_agentic_sdd_demo


def section_header(title: str):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def run_classic_demo():
    section_header("1. DEMO: SDD CLÁSSICO (ESTÁTICO & PASSIVO)")
    print("📜 O SDD clássico dependia de documentos Markdown/Wiki não compiláveis.")
    print("   Desenvolvedores liam o texto e escreviam código manualmente.")

    accounts = {
        "CONTA_ORIGEM": Account(account_id="CONTA_ORIGEM", balance=500.0),
        "CONTA_DESTINO": Account(account_id="CONTA_DESTINO", balance=100.0),
    }

    print(f"\nSaldos Iniciais: ORIGEM R$ {accounts['CONTA_ORIGEM'].balance:.2f} | DESTINO R$ {accounts['CONTA_DESTINO'].balance:.2f}")

    service = ClassicTransferService(accounts)
    success = service.execute_transfer("CONTA_ORIGEM", "CONTA_DESTINO", 150.0)

    print(f"Executando transferência de R$ 150.00... Resultado: {success}")
    print(f"Saldos Finais: ORIGEM R$ {accounts['CONTA_ORIGEM'].balance:.2f} | DESTINO R$ {accounts['CONTA_DESTINO'].balance:.2f}")
    print("\n⚠️ Fragilidade: Se o dev esquecer uma validação, a especificação em texto não impede a quebra.")


def run_executable_sdd_demo():
    section_header("2. DEMO: SDD EXECUTÁVEL (PYDANTIC + INVARIANTES)")
    print("📐 A especificação agora é CÓDIGO EXECUTÁVEL. Tipos e Invariantes são verificados em runtime.")

    initial_accs = {
        "ACC_X": AccountStateSpec(account_id="ACC_X", balance=Decimal("1000.00")),
        "ACC_Y": AccountStateSpec(account_id="ACC_Y", balance=Decimal("250.00")),
    }

    print(f"Contratos Pydantic validados na borda:")
    try:
        req = TransferRequestSpec(
            source_account_id="ACC_X",
            target_account_id="ACC_Y",
            amount=MoneyAmount(amount=Decimal("300.00"))
        )
        print(f" ✅ Requisição Válida: {req.source_account_id} -> {req.target_account_id} : R$ {req.amount.amount}")
    except Exception as e:
        print(f" ❌ Rejeitado na borda: {e}")

    # Demonstração de Invariante
    print("\nVerificando Invariante de Conservação de Dinheiro...")
    assert_conservation_of_money(initial_accs, initial_accs)
    assert_no_negative_balances(initial_accs)
    print(" ✅ Invariantes matemáticas validadas com sucesso!")


def run_agentic_harness_demo():
    section_header("3. DEMO: SDD AGÊNTICO NO HARNESS DE DESENVOLVIMENTO")
    print("🤖 O SDD torna-se o próprio Harness do Agente: Intenção + Continuous Evaluation Loop.")
    run_agentic_sdd_demo(max_iterations=3)


def main():
    print("🚀 INICIANDO WALKTHROUGH: A EVOLUÇÃO DO SDD NA ERA AGÊNTICA")
    run_classic_demo()
    run_executable_sdd_demo()
    run_agentic_harness_demo()

    print("\n" + "*" * 80)
    print("  ✨ TODOS OS EXEMPLOS FORAM EXECUTADOS COM SUCESSO!")
    print("  Para ler os artigos detalhados, consulte a pasta docs/:")
    print("    • docs/01-o-fim-do-sdd-estatico.md")
    print("    • docs/02-os-4-pilares-agentic-sdd.md")
    print("    • docs/03-harness-como-especificacao.md")
    print("*" * 80 + "\n")


if __name__ == "__main__":
    main()
