"""
Analisador de arquivos e empacotamento para workers.
"""

import os
from typing import List, Tuple, Optional

class FileAnalyzer:
    """Responsável pela contagem de linhas e empacotamento estruturado de arquivos."""

    @staticmethod
    def count_lines(file_path: str) -> int:
        """Conta a quantidade exata de linhas de um arquivo de forma resiliente."""
        if not os.path.exists(file_path):
            return 0
        try:
            with open(file_path, "rb") as f:
                lines = 0
                buf_size = 1024 * 1024
                read_byte = f.raw.read if hasattr(f, "raw") else f.read
                buf = read_byte(buf_size)
                while buf:
                    lines += buf.count(b"\n")
                    buf = read_byte(buf_size)
                # Se o arquivo não termina com quebra de linha mas tem conteúdo
                return lines if lines > 0 else (1 if os.path.getsize(file_path) > 0 else 0)
        except Exception:
            # Fallback seguro
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                return sum(1 for _ in f)

    @staticmethod
    def is_targeted_read(
        start_line: Optional[int],
        end_line: Optional[int],
        threshold: int
    ) -> bool:
        """Determina se a chamada é uma leitura pontual (offset/limit) dentro do limiar."""
        if start_line is not None and end_line is not None:
            if start_line > 0 and end_line >= start_line:
                delta = end_line - start_line
                return delta < threshold
        return False

    @staticmethod
    def package_to_xml(file_paths: List[str]) -> Tuple[str, int]:
        """
        Empacota arquivos em tags XML estruturadas:
        <file path="...">...</file>
        Retorna a string XML e o total consolidado de linhas.
        """
        payload = []
        total_lines = 0
        for path in file_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    lines = FileAnalyzer.count_lines(path)
                    total_lines += lines
                    payload.append(f'<file path="{path}" lines="{lines}">\n{content}\n</file>')
                except Exception as e:
                    payload.append(f'<file path="{path}" error="{str(e)}" />')
            else:
                payload.append(f'<file path="{path}" error="not_found" />')
        return "\n".join(payload), total_lines
