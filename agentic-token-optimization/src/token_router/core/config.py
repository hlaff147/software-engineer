"""
Configurações centrais do Token Router.
"""

import os
from dataclasses import dataclass

@dataclass(frozen=True)
class RouterConfig:
    """Configuração imutável do roteador de tokens."""
    
    # Limiar padrão de linhas para interceptação (arquivos com >= threshold são delegados)
    line_threshold: int = 350
    
    # Modelo padrão configurado para os workers leves
    default_worker_model: str = "gemini-2.5-flash"
    
    # Temperatura padrão para workers analíticos e geradores
    worker_temperature: float = 0.2
    
    # Modo verboso para logs
    verbose: bool = False

    @classmethod
    def from_env(cls) -> "RouterConfig":
        """Instancia a configuração a partir de variáveis de ambiente."""
        threshold_str = os.getenv("AGENT_DELEGATION_THRESHOLD", "350")
        try:
            threshold = int(threshold_str)
        except ValueError:
            threshold = 350

        model = os.getenv("AGENT_WORKER_MODEL", "gemini-2.5-flash")
        
        temp_str = os.getenv("AGENT_WORKER_TEMP", "0.2")
        try:
            temperature = float(temp_str)
        except ValueError:
            temperature = 0.2

        verbose = os.getenv("AGENT_ROUTER_VERBOSE", "0") in ("1", "true", "True")

        return cls(
            line_threshold=threshold,
            default_worker_model=model,
            worker_temperature=temperature,
            verbose=verbose,
        )
