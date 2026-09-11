"""
Interface de Linha de Comando (CLI) unificada do Token Router.
"""

import sys
import argparse
from token_router.core.config import RouterConfig
from token_router.core.router import TokenRouter
from token_router.workers.bulk_reader import BulkReaderWorker
from token_router.workers.code_writer import CodeWriterWorker

def cmd_check(args):
    """Comando de verificação de interceptação (usado pelos Pre-Tool Hooks)."""
    config = RouterConfig.from_env()
    if args.threshold:
        config = RouterConfig(
            line_threshold=args.threshold,
            default_worker_model=config.default_worker_model,
            worker_temperature=config.worker_temperature,
            verbose=config.verbose,
        )
    router = TokenRouter(config)
    decision = router.evaluate_read_request(
        file_path=args.file,
        start_line=args.start_line,
        end_line=args.end_line,
    )

    if decision.allowed:
        if args.verbose:
            print(f"[OK] Leitura permitida: {decision.reason}")
        sys.exit(0)
    else:
        print(f"[BLOQUEIO PRE-TOOL] {decision.reason}", file=sys.stderr)
        if decision.recommendation:
            print(f"\n{decision.recommendation}", file=sys.stderr)
        sys.exit(1)

def cmd_read(args):
    """Comando para acionar o Bulk Reader Worker."""
    config = RouterConfig.from_env()
    worker = BulkReaderWorker(model_name=config.default_worker_model, temperature=config.worker_temperature)
    result = worker.execute(question=args.question, file_paths=args.paths, mock=True)
    if args.xml:
        print(result["raw_xml"])
    else:
        print(result["summary"])

def cmd_write(args):
    """Comando para acionar o Code Writer Worker."""
    config = RouterConfig.from_env()
    worker = CodeWriterWorker(model_name=config.default_worker_model, temperature=config.worker_temperature)
    try:
        result = worker.execute(
            spec=args.spec,
            reference_path=args.reference,
            target_path=args.target,
            mock=True,
        )
        if result["written_to_disk"]:
            print(f"[SUCESSO] Código gerado gravado diretamente em: {result['target_path']}")
        else:
            print(result["code"])
    except Exception as e:
        print(f"[ERRO] Falha na geração: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Ponto de entrada principal da CLI."""
    parser = argparse.ArgumentParser(
        prog="token-router",
        description="CLI do Token Router - Otimizador de custos e contexto para agentes de código.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcomando: check
    check_p = subparsers.add_parser("check", help="Avalia se um arquivo excede o limiar de leitura direta.")
    check_p.add_argument("file", help="Caminho do arquivo a inspecionar.")
    check_p.add_argument("--start-line", type=int, default=None, help="Linha inicial (leitura direcionada).")
    check_p.add_argument("--end-line", type=int, default=None, help="Linha final (leitura direcionada).")
    check_p.add_argument("--threshold", type=int, default=None, help="Sobrescrever limiar de linhas padrão.")
    check_p.add_argument("-v", "--verbose", action="store_true", help="Exibe detalhes da autorização.")
    check_p.set_defaults(func=cmd_check)

    # Subcomando: read
    read_p = subparsers.add_parser("read", help="Delega leitura e síntese analítica para o worker leve.")
    read_p.add_argument("--question", required=True, help="Dúvida ou objetivo analítico da leitura.")
    read_p.add_argument("--paths", nargs="+", required=True, help="Arquivos a serem analisados.")
    read_p.add_argument("--xml", action="store_true", help="Exibe o payload XML empacotado.")
    read_p.set_defaults(func=cmd_read)

    # Subcomando: write
    write_p = subparsers.add_parser("write", help="Gera código via worker leve e grava direto em disco.")
    write_p.add_argument("--spec", required=True, help="Especificação ou requisitos do código.")
    write_p.add_argument("--reference", required=True, help="Arquivo de referência de padrões e estilo.")
    write_p.add_argument("--target", required=False, help="Caminho de saída para gravação em disco.")
    write_p.set_defaults(func=cmd_write)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
