"""
Contrato base para workers de delegação.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseWorker(ABC):
    """Interface abstrata definindo o ciclo de vida de um worker de delegação."""

    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.2):
        self.model_name = model_name
        self.temperature = temperature

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Executa a tarefa delegada e retorna o resultado estruturado."""
        pass
