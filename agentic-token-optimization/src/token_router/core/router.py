"""
Motor de decisão determinístico de roteamento de tokens.
"""

from dataclasses import dataclass
from typing import Optional
from token_router.core.config import RouterConfig
from token_router.core.analyzer import FileAnalyzer

@dataclass(frozen=True)
class RoutingDecision:
    """Resultado da análise de roteamento."""
    allowed: bool
    file_path: str
    line_count: int
    threshold: int
    reason: str
    recommendation: Optional[str] = None

class TokenRouter:
    """Aplica as políticas de interceptação de ferramentas."""

    def __init__(self, config: Optional[RouterConfig] = None):
        self.config = config or RouterConfig.from_env()

    def evaluate_read_request(
        self,
        file_path: str,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
    ) -> RoutingDecision:
        """
        Avalia se a leitura direta do arquivo deve ser permitida ou bloqueada.
        """
        # 1. Se a leitura for direcionada (offset/limit pequeno), autoriza
        if FileAnalyzer.is_targeted_read(start_line, end_line, self.config.line_threshold):
            return RoutingDecision(
                allowed=True,
                file_path=file_path,
                line_count=(end_line - start_line) if (end_line and start_line) else 0,
                threshold=self.config.line_threshold,
                reason="Targeted read permitido (intervalo menor que o limiar).",
            )

        # 2. Conta as linhas do arquivo
        line_count = FileAnalyzer.count_lines(file_path)

        # 3. Se arquivo for menor que o limiar, autoriza leitura direta
        if line_count < self.config.line_threshold:
            return RoutingDecision(
                allowed=True,
                file_path=file_path,
                line_count=line_count,
                threshold=self.config.line_threshold,
                reason="Arquivo dentro do limiar aceitável para o modelo de fronteira.",
            )

        # 4. Arquivo grande demais -> BLOQUEIA determinístico
        rec = (
            f"O arquivo {file_path} possui {line_count} linhas (limite: {self.config.line_threshold}).\n"
            f"A leitura direta foi bloqueada para economizar tokens.\n"
            f"Use o utilitário de delegação: token-router read --paths \"{file_path}\" --question \"<pergunta>\"\n"
            f"Ou realize uma leitura direcionada com parâmetros de linha (menos de {self.config.line_threshold} linhas)."
        )

        return RoutingDecision(
            allowed=False,
            file_path=file_path,
            line_count=line_count,
            threshold=self.config.line_threshold,
            reason="Excedeu o limiar de linhas para leitura direta.",
            recommendation=rec,
        )
