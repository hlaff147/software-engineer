"""
Token Router - Otimizador e roteador de tokens para agentes de código autônomos.
"""

__version__ = "0.1.0"
__author__ = "Humberto Filho"

from token_router.core.config import RouterConfig
from token_router.core.analyzer import FileAnalyzer
from token_router.core.router import TokenRouter
from token_router.workers.bulk_reader import BulkReaderWorker
from token_router.workers.code_writer import CodeWriterWorker

__all__ = [
    "RouterConfig",
    "FileAnalyzer",
    "TokenRouter",
    "BulkReaderWorker",
    "CodeWriterWorker",
]
