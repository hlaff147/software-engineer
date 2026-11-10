#!/usr/bin/env python3
"""
Simulador de Arquitetura e Pipeline das 6 Estratégias de Otimização de Custos em IA:
1. Prompt Caching (KV Cache de Prefixo Estável)
2. Model Routing (Roteamento entre Modelo Pequeno e Modelo de Fronteira)
3. Batch API (Processamento Assíncrono em Lote com Desconto)
4. Semantic Cache (Cache Vetorial por Similaridade de Cosseno)
5. Trim the Context (Janela Deslizante + Sumarização + Recuperação Relevante)
6. Go Smaller / Smaller Models (Destilação 70B -> 8B + Quantização 4-bit INT4)
"""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


# ============================================================================
# TABELA DE PREÇOS DE REFERÊNCIA (USD por 1 Milhão de Tokens)
# ============================================================================

class ModelTier(Enum):
    FRONTIER = "frontier-70b-pro"          # Ex: GPT-4o / Claude Sonnet / Gemini Pro
    SMALL_FLASH = "small-flash-mini"       # Ex: GPT-4o-mini / Gemini Flash / Haiku
    DISTILLED_8B_INT4 = "distilled-8b-4bit"  # Modelo 8B destilado e quantizado em 4-bit


@dataclass(frozen=True)
class ModelPricing:
    name: str
    input_per_1m: float
    output_per_1m: float
    cached_input_discount: float = 0.75  # 75% de desconto nos tokens em KV Cache


PRICING_CATALOG: Dict[ModelTier, ModelPricing] = {
    ModelTier.FRONTIER: ModelPricing(
        name="Frontier Model (Pro/Opus)",
        input_per_1m=5.00,
        output_per_1m=15.00,
        cached_input_discount=0.75,
    ),
    ModelTier.SMALL_FLASH: ModelPricing(
        name="Small Commercial Model (Flash/Mini)",
        input_per_1m=0.15,
        output_per_1m=0.60,
        cached_input_discount=0.75,
    ),
    ModelTier.DISTILLED_8B_INT4: ModelPricing(
        name="Distilled 8B Model (4-bit Quantized)",
        input_per_1m=0.04,
        output_per_1m=0.10,
        cached_input_discount=0.75,
    ),
}


# ============================================================================
# ESTRATÉGIA 1: PROMPT CACHING (KV CACHE DE PREFIXO ESTÁVEL)
# ============================================================================

class PromptCacheManager:
    """
    Simula o KV Cache de prefixo estável (system prompt + tool schemas).
    Garante que prefixos idênticos reutilizem os tensores K/V sem recomputação.
    """

    def __init__(self, min_cacheable_tokens: int = 1024) -> None:
        self.min_cacheable_tokens = min_cacheable_tokens
        self._active_prefixes: set[str] = set()
        self.hits: int = 0
        self.misses: int = 0

    @staticmethod
    def hash_prefix(system_prompt: str, tool_schemas: str) -> str:
        canonical = f"{system_prompt.strip()}||{tool_schemas.strip()}"
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def check_and_register_prefix(
        self, system_prompt: str, tool_schemas: str, prefix_tokens: int
    ) -> Tuple[bool, int, int]:
        """
        Retorna (is_cache_hit, cached_tokens, uncached_prefix_tokens).
        """
        if prefix_tokens < self.min_cacheable_tokens:
            self.misses += 1
            return False, 0, prefix_tokens

        prefix_hash = self.hash_prefix(system_prompt, tool_schemas)
        if prefix_hash in self._active_prefixes:
            self.hits += 1
            return True, prefix_tokens, 0

        self._active_prefixes.add(prefix_hash)
        self.misses += 1
        return False, 0, prefix_tokens


# ============================================================================
# ESTRATÉGIA 2: MODEL ROUTING (ROTEADOR DE COMPLEXIDADE E TAREFA)
# ============================================================================

class ModelRouter:
    """
    Classifica a requisição e envia cada query para o modelo mais econômico
    que consegue atendê-la mantendo qualidade de produção.
    """

    HARD_KEYWORDS = {
        "arquitetura", "concorrência", "race condition", "otimize", "prova matemática",
        "distribuído", "consenso", "raft", "deadlock", "refatore", "segurança crítica",
    }
    NARROW_TASK_KEYWORDS = {
        "classifique", "extraia json", "sentimento", "categoria", "cpf", "nota fiscal",
    }

    def route(self, query: str, allow_distilled: bool = True) -> ModelTier:
        normalized = query.lower()

        # 1. Tarefas estreitas (narrow tasks) -> Modelo 8B Destilado + Quantizado 4-bit
        if allow_distilled and any(kw in normalized for kw in self.NARROW_TASK_KEYWORDS):
            return ModelTier.DISTILLED_8B_INT4

        # 2. Queries complexas de engenharia / raciocínio profundo -> Frontier Model
        if any(kw in normalized for kw in self.HARD_KEYWORDS) or len(query) > 350:
            return ModelTier.FRONTIER

        # 3. Consultas simples do dia a dia (maioria do tráfego) -> Small Flash Model
        return ModelTier.SMALL_FLASH


# ============================================================================
# ESTRATÉGIA 3: BATCH API (PROCESSAMENTO ASSÍNCRONO EM LOTE <= 24H)
# ============================================================================

@dataclass
class BatchRequestItem:
    custom_id: str
    prompt_tokens: int
    output_tokens: int
    model_tier: ModelTier = ModelTier.SMALL_FLASH


class BatchAPIProcessor:
    """
    Agrupa grandes volumes de requisições assíncronas (SLAs <= 24h)
    aplicando o desconto padrão de 50% oferecido pelos provedores de nuvem.
    """

    BATCH_DISCOUNT = 0.50  # 50% off em tokens de entrada e saída

    def __init__(self) -> None:
        self._queue: List[BatchRequestItem] = []

    def enqueue(self, item: BatchRequestItem) -> None:
        self._queue.append(item)

    def flush_batch(self) -> Tuple[int, float, float]:
        """
        Processa todos os itens da fila e retorna:
        (quantidade_processada, custo_sincrono_padrao, custo_com_batch_api)
        """
        count = len(self._queue)
        standard_cost = 0.0
        for item in self._queue:
            pricing = PRICING_CATALOG[item.model_tier]
            cost = (
                (item.prompt_tokens / 1_000_000) * pricing.input_per_1m
                + (item.output_tokens / 1_000_000) * pricing.output_per_1m
            )
            standard_cost += cost

        batch_cost = standard_cost * (1.0 - self.BATCH_DISCOUNT)
        self._queue.clear()
        return count, standard_cost, batch_cost


# ============================================================================
# ESTRATÉGIA 4: SEMANTIC CACHE (CACHE VETORIAL COM EMBEDDINGS)
# ============================================================================

class SemanticCache:
    """
    Cache semântico que converte queries em vetores normalizados e reutiliza
    respostas quando a Similaridade de Cosseno >= threshold (ex: 0.85).
    Inclui validação de escopo (tenant) e proteção contra colisão de números/datas.
    """

    STOPWORDS = {
        "o", "a", "os", "as", "de", "do", "da", "em", "no", "na", "para", "com",
        "como", "eu", "posso", "faço", "qual", "é", "um", "uma", "por", "favor",
        "me", "ajude", "quero", "preciso", "meu", "minha", "no", "app", "aplicativo",
    }

    SYNONYM_MAP = {
        "resetar": "redefinir",
        "trocar": "redefinir",
        "alterar": "redefinir",
        "mudar": "redefinir",
        "esqueci": "redefinir",
        " recuperar": "redefinir",
        "boleto": "fatura",
        "conta": "fatura",
        "segunda": "2a",
    }

    def __init__(self, similarity_threshold: float = 0.82) -> None:
        self.similarity_threshold = similarity_threshold
        self._store: List[Tuple[str, Dict[str, float], set[str], str]] = []
        self.hits = 0
        self.misses = 0

    @classmethod
    def _extract_tokens(cls, text: str) -> Tuple[List[str], set[str]]:
        cleaned = re.sub(r"[^\w\s]", " ", text.lower())
        raw_tokens = cleaned.split()
        # Números/anos exatos funcionam como âncoras rígidas para evitar falso positivo
        numeric_anchors = {t for t in raw_tokens if any(ch.isdigit() for ch in t)}
        semantic_tokens = []
        for t in raw_tokens:
            if t in cls.STOPWORDS:
                continue
            canonical = cls.SYNONYM_MAP.get(t, t)
            # Stemming simplificado de sufixos comuns em pt-BR
            if len(canonical) > 5 and canonical.endswith(("ar", "er", "ir", "os", "as")):
                canonical = canonical[:-2]
            semantic_tokens.append(canonical)
        return semantic_tokens, numeric_anchors

    @classmethod
    def embed(cls, text: str) -> Tuple[Dict[str, float], set[str]]:
        """
        Gera representação vetorial esparsa (unigramas + bigramas de caracteres dos radicais)
        normalizada em norma L2 para cálculo exato de similaridade de cosseno.
        """
        tokens, numeric_anchors = cls._extract_tokens(text)
        features: Dict[str, float] = {}
        for tok in tokens:
            features[f"w:{tok}"] = features.get(f"w:{tok}", 0.0) + 2.0
            for i in range(len(tok) - 2):
                trigram = f"c:{tok[i:i+3]}"
                features[trigram] = features.get(trigram, 0.0) + 0.5

        norm = math.sqrt(sum(v * v for v in features.values())) or 1.0
        normalized = {k: v / norm for k, v in features.items()}
        return normalized, numeric_anchors

    @staticmethod
    def cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        if not vec_a or not vec_b:
            return 0.0
        # Produto escalar de vetores já normalizados em L2
        if len(vec_a) > len(vec_b):
            vec_a, vec_b = vec_b, vec_a
        return sum(val * vec_b.get(key, 0.0) for key, val in vec_a.items())

    def lookup(self, query: str, tenant_id: str = "global") -> Tuple[Optional[str], float]:
        query_vec, query_nums = self.embed(query)
        best_score = 0.0
        best_answer: Optional[str] = None

        for cached_tenant, cached_vec, cached_nums, answer in self._store:
            if cached_tenant != tenant_id:
                continue
            # Proteção contra falso positivo em datas/valores numéricos divergentes
            if query_nums != cached_nums:
                continue
            score = self.cosine_similarity(query_vec, cached_vec)
            if score > best_score:
                best_score = score
                best_answer = answer

        if best_score >= self.similarity_threshold and best_answer is not None:
            self.hits += 1
            return best_answer, best_score

        self.misses += 1
        return None, best_score

    def store(self, query: str, answer: str, tenant_id: str = "global") -> None:
        query_vec, query_nums = self.embed(query)
        self._store.append((tenant_id, query_vec, query_nums, answer))


# ============================================================================
# ESTRATÉGIA 5: TRIM THE CONTEXT (PODA E COMPRESSÃO DE HISTÓRICO)
# ============================================================================

@dataclass
class ConversationMessage:
    role: str
    content: str
    tokens: int
    is_tool_output: bool = False


class ContextTrimmer:
    """
    Evita reenviar o histórico completo da conversa a cada turno:
    1. Aplica poda em payloads antigos de ferramentas (Tool Output Pruning)
    2. Sumariza mensagens antigas fora da janela deslizante
    3. Mantém intactas apenas as últimas `window_size` mensagens + fatos relevantes
    """

    def __init__(self, window_size: int = 4, summary_fixed_tokens: int = 150) -> None:
        self.window_size = window_size
        self.summary_fixed_tokens = summary_fixed_tokens

    def trim(self, history: List[ConversationMessage]) -> Tuple[int, int]:
        """
        Retorna (raw_history_tokens, trimmed_history_tokens).
        """
        raw_tokens = sum(msg.tokens for msg in history)
        if len(history) <= self.window_size:
            return raw_tokens, raw_tokens

        older_messages = history[: -self.window_size]
        recent_messages = history[-self.window_size :]

        # Mensagens antigas viram um resumo compacto único (rolling summary)
        compressed_old_tokens = min(
            sum(m.tokens for m in older_messages), self.summary_fixed_tokens
        )

        # Nas mensagens recentes, truncamos saídas brutas gigantes de tools já consumidas
        recent_tokens = 0
        for idx, msg in enumerate(recent_messages):
            if msg.is_tool_output and idx < len(recent_messages) - 1:
                recent_tokens += min(msg.tokens, 120)  # Mantém apenas resumo da tool
            else:
                recent_tokens += msg.tokens

        trimmed_tokens = compressed_old_tokens + recent_tokens
        return raw_tokens, trimmed_tokens


# ============================================================================
# ESTRATÉGIA 6: GO SMALLER (DESTILAÇÃO E QUANTIZAÇÃO DE MODELOS)
# ============================================================================

@dataclass(frozen=True)
class ModelCompressionReport:
    teacher_params_b: float
    student_params_b: float
    teacher_vram_fp16_gb: float
    student_vram_int4_gb: float
    vram_reduction_pct: float
    retained_accuracy_pct: float
    cost_reduction_pct: float


def evaluate_model_distillation_and_quantization(
    teacher_params_b: float = 70.0,
    student_params_b: float = 8.0,
    quantization_bits: int = 4,
) -> ModelCompressionReport:
    """
    Calcula a redução de VRAM e custo ao destilar um modelo 70B (FP16)
    para um modelo menor (ex: 8B) e quantizá-lo em 4-bit (AWQ/GPTQ).
    """
    # Em FP16 (2 bytes/parâmetro) + ~20% de overhead de execução/ativação
    teacher_vram_gb = teacher_params_b * 2.0 * 1.2
    bytes_per_param_quant = quantization_bits / 8.0
    student_vram_gb = student_params_b * bytes_per_param_quant * 1.2

    vram_reduction = (1.0 - (student_vram_gb / teacher_vram_gb)) * 100.0
    # 4-bit AWQ/GPTQ preserva ~99% da acurácia em tarefas estreitas destiladas
    accuracy_map = {16: 99.6, 8: 99.4, 4: 99.0}
    retained_acc = accuracy_map.get(quantization_bits, 95.0)

    frontier_price = PRICING_CATALOG[ModelTier.FRONTIER].input_per_1m
    distilled_price = PRICING_CATALOG[ModelTier.DISTILLED_8B_INT4].input_per_1m
    cost_reduction = (1.0 - (distilled_price / frontier_price)) * 100.0

    return ModelCompressionReport(
        teacher_params_b=teacher_params_b,
        student_params_b=student_params_b,
        teacher_vram_fp16_gb=round(teacher_vram_gb, 2),
        student_vram_int4_gb=round(student_vram_gb, 2),
        vram_reduction_pct=round(vram_reduction, 2),
        retained_accuracy_pct=retained_acc,
        cost_reduction_pct=round(cost_reduction, 2),
    )


# ============================================================================
# PIPELINE UNIFICADO EM PRODUÇÃO (DEFENSE-IN-DEPTH COST GATEWAY)
# ============================================================================

@dataclass
class SimulationMetrics:
    baseline_cost_usd: float = 0.0
    optimized_cost_usd: float = 0.0
    semantic_cache_hits: int = 0
    prompt_cache_hits: int = 0
    routed_to_distilled: int = 0
    routed_to_small: int = 0
    routed_to_frontier: int = 0
    batch_jobs_processed: int = 0
    tokens_saved_by_trimming: int = 0

    @property
    def total_savings_usd(self) -> float:
        return max(0.0, self.baseline_cost_usd - self.optimized_cost_usd)

    @property
    def savings_percentage(self) -> float:
        if self.baseline_cost_usd <= 0:
            return 0.0
        return (self.total_savings_usd / self.baseline_cost_usd) * 100.0


class AICostOptimizationGateway:
    """
    Integra as 6 estratégias de otimização em um único pipeline de produção.
    """

    def __init__(self) -> None:
        self.prompt_cache = PromptCacheManager(min_cacheable_tokens=1024)
        self.semantic_cache = SemanticCache(similarity_threshold=0.82)
        self.router = ModelRouter()
        self.trimmer = ContextTrimmer(window_size=4, summary_fixed_tokens=150)
        self.batch_processor = BatchAPIProcessor()
        self.metrics = SimulationMetrics()

    def process_online_request(
        self,
        query: str,
        system_prompt: str,
        tool_schemas: str,
        prefix_tokens: int,
        history: List[ConversationMessage],
        query_tokens: int,
        expected_output_tokens: int,
        tenant_id: str = "global",
    ) -> float:
        # 1. Cálculo do Baseline (Sem otimização: Frontier Model + Histórico Completo + Sem Cache)
        raw_history_tokens = sum(m.tokens for m in history)
        baseline_input_tokens = prefix_tokens + raw_history_tokens + query_tokens
        frontier_pricing = PRICING_CATALOG[ModelTier.FRONTIER]
        baseline_req_cost = (
            (baseline_input_tokens / 1_000_000) * frontier_pricing.input_per_1m
            + (expected_output_tokens / 1_000_000) * frontier_pricing.output_per_1m
        )
        self.metrics.baseline_cost_usd += baseline_req_cost

        # 2. [Estratégia #4] Semantic Cache Lookup
        cached_answer, _ = self.semantic_cache.lookup(query, tenant_id=tenant_id)
        if cached_answer is not None:
            self.metrics.semantic_cache_hits += 1
            # Custo de embedding local/leve é desprezível (~$0.000001)
            return 0.0

        # 3. [Estratégia #5] Trim the Context (Poda de Histórico e Tools)
        raw_hist, trimmed_hist = self.trimmer.trim(history)
        self.metrics.tokens_saved_by_trimming += raw_hist - trimmed_hist

        # 4. [Estratégia #1] Prompt Caching (KV Cache de Prefixo Estático)
        is_kv_hit, cached_prefix_tk, uncached_prefix_tk = (
            self.prompt_cache.check_and_register_prefix(
                system_prompt, tool_schemas, prefix_tokens
            )
        )
        if is_kv_hit:
            self.metrics.prompt_cache_hits += 1

        # 5. [Estratégia #2 & #6] Model Routing + Smaller Distilled Model
        selected_tier = self.router.route(query, allow_distilled=True)
        if selected_tier == ModelTier.DISTILLED_8B_INT4:
            self.metrics.routed_to_distilled += 1
        elif selected_tier == ModelTier.SMALL_FLASH:
            self.metrics.routed_to_small += 1
        else:
            self.metrics.routed_to_frontier += 1

        pricing = PRICING_CATALOG[selected_tier]

        # Cálculo do custo otimizado considerando desconto de KV Cache no prefixo
        cached_rate = pricing.input_per_1m * (1.0 - pricing.cached_input_discount)
        uncached_input_tokens = uncached_prefix_tk + trimmed_hist + query_tokens

        optimized_req_cost = (
            (cached_prefix_tk / 1_000_000) * cached_rate
            + (uncached_input_tokens / 1_000_000) * pricing.input_per_1m
            + (expected_output_tokens / 1_000_000) * pricing.output_per_1m
        )

        # Armazena a resposta no Semantic Cache para perguntas similares futuras
        self.semantic_cache.store(query, f"Resposta para: {query}", tenant_id=tenant_id)
        self.metrics.optimized_cost_usd += optimized_req_cost
        return optimized_req_cost


def run_production_simulation() -> None:
    gateway = AICostOptimizationGateway()

    static_system_prompt = "Você é um assistente corporativo especialista em finanças e engenharia."
    static_tool_schemas = '{"tools": [{"name": "get_invoice"}, {"name": "reset_password"}]}'
    prefix_tokens = 4000

    # Histórico longo de 16 mensagens simulando sessão multi-turn com chamadas de tools
    sample_long_history = [
        ConversationMessage("user", f"Mensagem antiga {i}", tokens=250)
        for i in range(12)
    ] + [
        ConversationMessage("tool", "Payload JSON grande de tool", tokens=2400, is_tool_output=True),
        ConversationMessage("assistant", "Resumo entregue", tokens=200),
        ConversationMessage("user", "Dúvida recente", tokens=200),
        ConversationMessage("assistant", "Resposta recente", tokens=200),
    ]

    workload = [
        # (query, repetições, espera_tokens_saida)
        ("Como faço para resetar minha senha no aplicativo?", 180, 150),
        ("Esqueci minha senha do app, como posso redefinir?", 170, 150),
        ("Como emitir a segunda via do boleto da minha conta?", 150, 150),
        ("Preciso tirar a 2a via da fatura, como faço?", 150, 150),
        ("Classifique o sentimento e extraia JSON desta nota fiscal #9912", 200, 120),
        (
            "Projete uma arquitetura distribuída com consenso Raft para evitar race condition e deadlock",
            150,
            600,
        ),
    ]

    for query, count, out_tokens in workload:
        for _ in range(count):
            gateway.process_online_request(
                query=query,
                system_prompt=static_system_prompt,
                tool_schemas=static_tool_schemas,
                prefix_tokens=prefix_tokens,
                history=sample_long_history,
                query_tokens=60,
                expected_output_tokens=out_tokens,
            )

    # Adiciona 500 jobs assíncronos de classificação em lote via Batch API (Estratégia #3)
    frontier_pricing = PRICING_CATALOG[ModelTier.FRONTIER]
    for i in range(500):
        prompt_tk, out_tk = 3000, 200
        # No baseline sem otimização, rodaria síncrono no modelo Frontier
        gateway.metrics.baseline_cost_usd += (
            (prompt_tk / 1_000_000) * frontier_pricing.input_per_1m
            + (out_tk / 1_000_000) * frontier_pricing.output_per_1m
        )
        gateway.batch_processor.enqueue(
            BatchRequestItem(
                custom_id=f"job-{i}",
                prompt_tokens=prompt_tk,
                output_tokens=out_tk,
                model_tier=ModelTier.SMALL_FLASH,
            )
        )

    batch_count, _, batch_cost = gateway.batch_processor.flush_batch()
    gateway.metrics.batch_jobs_processed = batch_count
    gateway.metrics.optimized_cost_usd += batch_cost

    compression = evaluate_model_distillation_and_quantization()
    m = gateway.metrics

    print("=" * 84)
    print(" 💰 SIMULADOR DE OTIMIZAÇÃO DE CUSTOS EM SISTEMAS DE IA (6 ESTRATÉGIAS)")
    print("=" * 84)
    print(f"Requisições Online Processadas : 1.000 | Jobs em Batch (<=24h) : {m.batch_jobs_processed}")
    print(f"Prefixo Estático (System+Tools): {prefix_tokens} tk | Histórico Bruto: 6.000 tk")
    print("-" * 84)
    print(f"1. [Prompt Caching]   KV Cache Hits no Prefixo     : {m.prompt_cache_hits} hits (75% off no prefixo)")
    print(f"2. [Model Routing]    Small Flash: {m.routed_to_small} | 8B INT4: {m.routed_to_distilled} | Frontier: {m.routed_to_frontier}")
    print(f"3. [Batch API]        Jobs Assíncronos com 50% Off : {m.batch_jobs_processed} requisições")
    print(f"4. [Semantic Cache]   Respostas Reutilizadas (Hit) : {m.semantic_cache_hits} hits ($0 custo de LLM)")
    print(f"5. [Trim the Context] Tokens de Histórico Poupados : {m.tokens_saved_by_trimming:,} tokens")
    print(
        f"6. [Go Smaller 4-bit] 70B FP16 ({compression.teacher_vram_fp16_gb} GB) -> "
        f"8B INT4 ({compression.student_vram_int4_gb} GB VRAM, -{compression.vram_reduction_pct}% VRAM, "
        f"~{compression.retained_accuracy_pct}% acc)"
    )
    print("-" * 84)
    print(f"🔴 Custo Baseline (Sem Otimização) : $ {m.baseline_cost_usd:10.4f}")
    print(f"🟢 Custo Pipeline Otimizado (6x)   : $ {m.optimized_cost_usd:10.4f}")
    print(f"🔥 Economia Total Obtida           :   {m.savings_percentage:9.2f}% ($ {m.total_savings_usd:.4f} poupados)")
    print("=" * 84)


if __name__ == "__main__":
    run_production_simulation()
