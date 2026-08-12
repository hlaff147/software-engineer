#!/usr/bin/env python3
"""
floating_point_drift.py
-----------------------
Demonstração de perda de precisão em ponto flutuante (IEEE 754) vs soluções
de software (Decimal e Fraction) em Python.
"""

import time
from decimal import Decimal, getcontext
from fractions import Fraction

# Configurando precisão padrão do módulo decimal (28 dígitos padrão)
getcontext().prec = 28


def banner(titulo: str):
    print("\n" + "=" * 70)
    print(f" 🧪 {titulo.upper()}")
    print("=" * 70)


def experimento_1_float_nativo(incremento: float = 0.0001, passos: int = 1_000_000):
    """
    Experimento 1: Soma acumulada usando o tipo float (IEEE 754 64-bit nativo da CPU).
    """
    banner("Experimento 1: float Nativo (IEEE 754)")
    print(f"Somando {incremento} exatamente {passos:_} vezes...\n")

    inicio = time.perf_counter()
    soma = 0.0
    for _ in range(passos):
        soma += incremento
    fim = time.perf_counter()

    esperado = incremento * passos
    erro_absoluto = abs(soma - esperado)
    erro_relativo_pct = (erro_absoluto / esperado) * 100

    print(f"• Resultado real acumulado (`float`):  {soma:.17f}")
    print(f"• Resultado matemático esperado:      {esperado:.17f}")
    print(f"• Erro absoluto acumulado:            {erro_absoluto:.17e}")
    print(f"• Erro relativo (%):                  {erro_relativo_pct:.15f}%")
    print(f"• Tempo de execução:                  {(fim - inicio)*1000:.2f} ms")


def experimento_2_soma_simples():
    """
    Experimento 2: A clássica inconsistência 0.1 + 0.2 != 0.3.
    """
    banner("Experimento 2: A Inconsistência 0.1 + 0.2 != 0.3")

    a, b = 0.1, 0.2
    soma_float = a + b
    esperado = 0.3

    print(f"• 0.1 no float 64-bit:   {a:.17f}")
    print(f"• 0.2 no float 64-bit:   {b:.17f}")
    print(f"• 0.1 + 0.2 real:        {soma_float:.17f}")
    print(f"• 0.3 esperado:          {esperado:.17f}")
    print(f"• 0.1 + 0.2 == 0.3 ?     {soma_float == esperado}")


def experimento_3_decimal(incremento_str: str = "0.0001", passos: int = 1_000_000):
    """
    Experimento 3: Solução usando decimal.Decimal (Ponto Fixo Decimal de Precisão Arbitrária).
    """
    banner("Experimento 3: Solução com decimal.Decimal")
    print(f"Somando Decimal('{incremento_str}') exatamente {passos:_} vezes...\n")

    incremento = Decimal(incremento_str)
    inicio = time.perf_counter()
    soma = Decimal("0.0")
    for _ in range(passos):
        soma += incremento
    fim = time.perf_counter()

    esperado = incremento * passos
    erro_absoluto = abs(soma - esperado)

    print(f"• Resultado acumulado (`Decimal`):    {soma}")
    print(f"• Resultado matemático esperado:      {esperado}")
    print(f"• Erro absoluto acumulado:            {erro_absoluto}")
    print(f"• Tempo de execução:                  {(fim - inicio)*1000:.2f} ms")


def experimento_4_fractions(incremento_num: int = 1, incremento_den: int = 10000, passos: int = 1_000_000):
    """
    Experimento 4: Solução usando fractions.Fraction (Números Racionais Exatos).
    """
    banner("Experimento 4: Solução com fractions.Fraction")
    print(f"Somando Fraction({incremento_num}, {incremento_den}) exatamente {passos:_} vezes...\n")

    incremento = Fraction(incremento_num, incremento_den)
    inicio = time.perf_counter()
    soma = Fraction(0, 1)
    for _ in range(passos):
        soma += incremento
    fim = time.perf_counter()

    esperado = incremento * passos
    erro_absoluto = abs(soma - esperado)

    print(f"• Resultado acumulado (`Fraction`):   {soma} ({float(soma)})")
    print(f"• Resultado matemático esperado:      {esperado} ({float(esperado)})")
    print(f"• Erro absoluto acumulado:            {erro_absoluto}")
    print(f"• Tempo de execução:                  {(fim - inicio)*1000:.2f} ms")


if __name__ == "__main__":
    print("🚀 INICIANDO BATERIA DE TESTES DE PONTO FLUTUANTE 🚀")
    experimento_1_float_nativo()
    experimento_2_soma_simples()
    experimento_3_decimal()
    experimento_4_fractions()
    print("\n" + "=" * 70)
    print(" ✅ BATERIA CONCLUÍDA COM SUCESSO!")
    print("=" * 70 + "\n")
