#!/usr/bin/env python3
"""
bulk-read.py - Utilitário de delegação de I/O para worker analítico leve.

Empacota múltiplos arquivos em tags XML estruturadas e delega a síntese para
um modelo worker de baixo custo, devolvendo apenas tópicos densos para o stdout.
"""

import sys
import argparse
import os

def build_xml_payload(file_paths):
    payload = []
    total_lines = 0
    for path in file_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            lines = content.count("\n") + 1
            total_lines += lines
            payload.append(f'<file path="{path}" lines="{lines}">\n{content}\n</file>')
        else:
            payload.append(f'<file path="{path}" error="not_found" />')
    return "\n".join(payload), total_lines

def simulate_worker_response(question, file_paths, total_lines):
    """
    Simulação didática / offline do retorno do worker.
    Em ambiente produtivo, substitua pela chamada da API do seu worker leve (Flash, Mini, SLM local).
    """
    summary = []
    summary.append(f"• Analisados {len(file_paths)} arquivos ({total_lines} linhas brutas processadas fora do modelo principal).")
    summary.append(f"• Resposta sintética à pergunta: '{question}'")
    for p in file_paths:
        base = os.path.basename(p)
        summary.append(f"  - [{base}]: Estrutura principal mapeada com sucesso.")
    return "\n".join(summary)

def main():
    parser = argparse.ArgumentParser(description="Delega I/O pesado de leitura para worker leve")
    parser.add_argument("--question", required=True, help="Pergunta analítica sobre o código")
    parser.add_argument("--paths", nargs="+", required=True, help="Lista de arquivos a serem analisados")
    parser.add_argument("--raw-xml", action="store_true", help="Apenas exibe o payload XML empacotado")
    args = parser.parse_args()

    files_xml, total_lines = build_xml_payload(args.paths)

    if args.raw_xml:
        print(files_xml)
        return

    # Em produção, aqui ocorre o dispatch para o runtime efêmero
    response = simulate_worker_response(args.question, args.paths, total_lines)
    print(response)

if __name__ == "__main__":
    main()
