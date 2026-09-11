#!/usr/bin/env python3
"""
code-write.py - Utilitário de geração de código padronizado direto em disco.

Recebe uma especificação funcional e um arquivo de referência, delega a geração
para um worker com contrato "code only" e grava o resultado diretamente no disco,
impedindo que o código gerado consuma a janela de contexto do modelo principal.
"""

import sys
import argparse
import os
import re

def clean_markdown_fences(content: str) -> str:
    """Remove eventuais blocos de código markdown que o modelo possa ter inserido."""
    content = content.strip()
    match = re.match(r"^```[a-zA-Z0-9_-]*\n(.*)\n```$", content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return content

def main():
    parser = argparse.ArgumentParser(description="Gera código via worker e grava direto no disco")
    parser.add_argument("--spec", required=True, help="Especificação ou requisitos do código")
    parser.add_argument("--reference", required=True, help="Arquivo de referência com padrões a seguir")
    parser.add_argument("--target", required=False, help="Caminho de destino do arquivo a ser gravado")
    args = parser.parse_args()

    if not os.path.exists(args.reference):
        print(f"Erro: Arquivo de referência '{args.reference}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    with open(args.reference, "r", encoding="utf-8", errors="replace") as f:
        reference_content = f.read()

    # Template do prompt para o worker leve
    system_prompt = (
        "Você gera arquivos de código completos baseando-se estritamente na especificação e na referência. "
        "Retorne APENAS o código executável. Sem markdown, sem saudações, sem explicações."
    )

    # Exemplo simulado de geração direta
    generated_code = f"""// Código gerado automaticamente a partir da referência: {os.path.basename(args.reference)}
// Spec: {args.spec}

public class GeneratedWorkerStub {{
    // Implementação padronizada gerada diretamente no disco
    public void execute() {{
        // Lógica consistente com {os.path.basename(args.reference)}
    }}
}}
"""
    cleaned_code = clean_markdown_fences(generated_code)

    if args.target:
        os.makedirs(os.path.dirname(os.path.abspath(args.target)), exist_ok=True)
        with open(args.target, "w", encoding="utf-8") as f:
            f.write(cleaned_code)
        print(f"Código gravado com sucesso diretamente em: {args.target}")
    else:
        print(cleaned_code)

if __name__ == "__main__":
    main()
