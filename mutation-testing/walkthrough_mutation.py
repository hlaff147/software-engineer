#!/usr/bin/env python3
"""
Walkthrough Interativo de Teste Mutante (Mutation Testing).

Demonstração Prática:
1. Por que a Cobertura de Código Tradicional (Line Coverage) pode ser enganosa (100% nas duas suítes).
2. Como a Suíte Fraca deixa Mutantes SOBREVIVEREM (Baixo Mutation Score).
3. Como a Suíte Forte MATA todos os Mutantes (100% Mutation Score).
"""

import sys
from pathlib import Path

# Adiciona o diretório src e a raiz ao sys.path para importações limpas
sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from discount_calculator import DiscountCalculator


from src.mutants.mutant_boundary import MutantBoundaryCalculator
from src.mutants.mutant_operator import MutantOperatorCalculator
from src.mutants.mutant_constant import MutantConstantCalculator
from src.mutants.mutant_logical import MutantLogicalCalculator

from src.custom_mutator import MutationRunner
from tests.test_weak import run_weak_tests_on
from tests.test_strong import run_strong_tests_on


MUTANTS_MAP = {
    "Mutante 1 (ROR: '>=' para '>')": MutantBoundaryCalculator,
    "Mutante 2 (AOR: '-' para '+')": MutantOperatorCalculator,
    "Mutante 3 (CR: '0.10' para '0.15')": MutantConstantCalculator,
    "Mutante 4 (LCR: 'or' para 'and')": MutantLogicalCalculator,
}


def print_banner(title: str):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_report(suite_name: str, eval_data: dict):
    print(f"\n📊 Relatório de Mutação: {suite_name}")
    print("-" * 60)
    for mutant_name, info in eval_data["results"].items():
        status_icon = info["status"]
        print(f"  • {mutant_name:<45} -> {status_icon}")
    
    score = eval_data["mutation_score"]
    killed = eval_data["killed_count"]
    total = eval_data["total_mutants"]
    
    print("-" * 60)
    print(f"  📈 Mutantes Mortos: {killed}/{total}")
    print(f"  🏆 MUTATION SCORE FINAL: {score:.1f}%\n")


def main():
    print_banner("🧬 DEMONSTRAÇÃO PRÁTICA DE TESTE MUTANTE (MUTATION TESTING)")

    print("\n1️⃣  EXAMINANDO A SUÍTE DE TESTES FRACA (WEAK TEST SUITE)")
    print("   • Cobertura de Linhas (Line Coverage): 100%")
    print("   • Tipo de Assertions: Vagas / Superficiais (`assert result is not None`) ")
    
    weak_eval = MutationRunner.evaluate_suite_on_mutants(MUTANTS_MAP, run_weak_tests_on)
    print_report("SUÍTE FRACA", weak_eval)

    print_banner("2️⃣  EXAMINANDO A SUÍTE DE TESTES FORTE (STRONG TEST SUITE)")
    print("   • Cobertura de Linhas (Line Coverage): 100%")
    print("   • Tipo de Assertions: Estritas / Valores Exatos & Condições de Borda")

    strong_eval = MutationRunner.evaluate_suite_on_mutants(MUTANTS_MAP, run_strong_tests_on)
    print_report("SUÍTE FORTE", strong_eval)

    print_banner("💡 LIÇÃO APRENDIDA")
    print("  Ambas as suítes atingem 100% de Line Coverage.")
    print(f"  Porém, a Suíte Fraca obteve apenas {weak_eval['mutation_score']:.1f}% de Escore de Mutação (Mutantes Sobreviveram!),")
    print(f"  enquanto a Suíte Forte obteve {strong_eval['mutation_score']:.1f}% de Escore de Mutação (Todos os Mutantes Mortos!).")
    print("  O Teste Mutante é o verdadeiro medidor de qualidade e resiliência de testes.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
