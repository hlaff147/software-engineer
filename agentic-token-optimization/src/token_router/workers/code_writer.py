"""
Worker Gerador de Código Boilerplate (Code Writer).
"""

import os
import re
from typing import Dict, Any, Optional
from token_router.workers.base import BaseWorker

class CodeWriterWorker(BaseWorker):
    """
    Worker que gera código repetitivo baseado em uma especificação funcional e
    um arquivo de referência, com contrato "output only code" e gravação direta em disco.
    """

    SYSTEM_PROMPT = (
        "Você gera arquivos de código completos baseando-se estritamente na especificação e na referência. "
        "Reproduza os mesmos padrões, convenções e estilos do código de referência. "
        "Retorne EXCLUSIVAMENTE o código-fonte executável. "
        "PROIBIDO incluir formatação markdown (sem ```), explicações ou conversas."
    )

    @staticmethod
    def strip_markdown_fences(content: str) -> str:
        """Remove blocos de formatação markdown que possam ter sido inseridos pelo modelo."""
        content = content.strip()
        match = re.match(r"^```[a-zA-Z0-9_-]*\n(.*)\n```$", content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return content

    def execute(
        self,
        spec: str,
        reference_path: str,
        target_path: Optional[str] = None,
        mock: bool = True
    ) -> Dict[str, Any]:
        """
        Executa a geração de código e opcionalmente grava direto no disco.
        """
        if not os.path.exists(reference_path):
            raise FileNotFoundError(f"Arquivo de referência não encontrado: {reference_path}")

        ref_base = os.path.basename(reference_path)

        # Mock / Geração determinística baseada no template
        generated_code = f"""// ==============================================================================
// Código gerado de forma autônoma pelo worker 'code-writer'
// Baseado no padrão de: {ref_base}
// Requisito / Spec: {spec}
// ==============================================================================

package com.generated.service;

import java.util.Objects;

public class GeneratedServiceStub {{

    private final String specDescription = "{spec}";

    public boolean executeOperation() {{
        // Lógica padronizada conforme as convenções de {ref_base}
        return Objects.nonNull(specDescription);
    }}
}}
"""
        clean_code = self.strip_markdown_fences(generated_code)

        written_to_disk = False
        if target_path:
            os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(clean_code)
            written_to_disk = True

        return {
            "code": clean_code,
            "target_path": target_path,
            "written_to_disk": written_to_disk,
            "reference_file": reference_path,
            "model_used": self.model_name,
        }
