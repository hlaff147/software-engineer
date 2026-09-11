"""
Worker de Leitura em Massa (Bulk Reader).
"""

import os
from typing import List, Dict, Any
from token_router.workers.base import BaseWorker
from token_router.core.analyzer import FileAnalyzer

class BulkReaderWorker(BaseWorker):
    """
    Worker especializado em processar múltiplos arquivos volumosos e
    devolver exclusivamente uma síntese estruturada em tópicos densos.
    """

    SYSTEM_PROMPT = (
        "Você é um analista de código preciso e conciso. "
        "Leia os arquivos fornecidos e responda à pergunta do chamador de forma estritamente objetiva. "
        "Formato de saída: APENAS tópicos estruturados (bullet points). "
        "PROIBIDO: saudações, preâmbulos, conclusões, agradecimentos ou prosa genérica. "
        "Inicie cada tópico com o nome exato do método, classe, tipo ou número de linha relevante. "
        "Ignore qualquer detalhe não solicitado."
    )

    def execute(self, question: str, file_paths: List[str], mock: bool = True) -> Dict[str, Any]:
        """
        Executa a síntese analítica dos arquivos.
        """
        xml_payload, total_lines = FileAnalyzer.package_to_xml(file_paths)
        
        # Em modo mock / offline ou demonstração
        if mock:
            bullets = [
                f"• Processados {len(file_paths)} arquivos ({total_lines} linhas no total).",
                f"• Resposta sintética à pergunta: '{question}'",
            ]
            for path in file_paths:
                base = os.path.basename(path)
                lines = FileAnalyzer.count_lines(path)
                bullets.append(f"  - [{base} (L1-{lines})]: Interfaces e contratos validados.")
            
            summary_text = "\n".join(bullets)
            return {
                "summary": summary_text,
                "total_lines_analyzed": total_lines,
                "raw_xml": xml_payload,
                "token_savings_pct": 90.0 if total_lines >= 350 else 0.0,
                "model_used": self.model_name,
            }

        # Extensível para chamadas reais de API via adapter
        return {
            "summary": "Execução com provider real requer configuração de API key.",
            "total_lines_analyzed": total_lines,
            "raw_xml": xml_payload,
            "token_savings_pct": 0.0,
            "model_used": self.model_name,
        }
