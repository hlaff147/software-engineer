import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from examples.cost_optimization_pipeline import (
    AICostOptimizationGateway,
    BatchAPIProcessor,
    BatchRequestItem,
    ContextTrimmer,
    ConversationMessage,
    ModelRouter,
    ModelTier,
    PromptCacheManager,
    SemanticCache,
    evaluate_model_distillation_and_quantization,
)


class TestSixCostOptimizationStrategies(unittest.TestCase):
    def test_1_prompt_caching_hits_on_shared_prefix(self) -> None:
        cache = PromptCacheManager(min_cacheable_tokens=1024)
        sys_prompt = "System Prompt Estático"
        tools = '{"tools": ["search", "calc"]}'

        # Primeira chamada: Cache Miss (registra no KV cache)
        hit1, cached1, uncached1 = cache.check_and_register_prefix(sys_prompt, tools, 2048)
        self.assertFalse(hit1)
        self.assertEqual(cached1, 0)
        self.assertEqual(uncached1, 2048)

        # Segunda chamada com o mesmo prefixo: KV Cache Hit!
        hit2, cached2, uncached2 = cache.check_and_register_prefix(sys_prompt, tools, 2048)
        self.assertTrue(hit2)
        self.assertEqual(cached2, 2048)
        self.assertEqual(uncached2, 0)

    def test_2_model_routing_by_difficulty_and_narrow_task(self) -> None:
        router = ModelRouter()

        # Query simples -> Small Flash Model
        self.assertEqual(router.route("Qual o horário de funcionamento?"), ModelTier.SMALL_FLASH)

        # Tarefa específica/restrita -> Modelo 8B Destilado & Quantizado
        self.assertEqual(
            router.route("Classifique o sentimento e extraia JSON desta nota fiscal"),
            ModelTier.DISTILLED_8B_INT4,
        )

        # Query complexa -> Frontier Model
        self.assertEqual(
            router.route("Analise a condição de race condition e deadlock na arquitetura distribuída"),
            ModelTier.FRONTIER,
        )

    def test_3_batch_api_applies_50_percent_discount(self) -> None:
        processor = BatchAPIProcessor()
        processor.enqueue(
            BatchRequestItem(
                custom_id="req-1",
                prompt_tokens=1_000_000,
                output_tokens=1_000_000,
                model_tier=ModelTier.FRONTIER,
            )
        )
        count, std_cost, batch_cost = processor.flush_batch()
        self.assertEqual(count, 1)
        self.assertAlmostEqual(std_cost, 20.0)  # $5 input + $15 output
        self.assertAlmostEqual(batch_cost, 10.0)  # 50% de desconto = $10

    def test_4_semantic_cache_reuses_similar_queries_and_protects_numbers(self) -> None:
        sem_cache = SemanticCache(similarity_threshold=0.80)
        sem_cache.store(
            "Como faço para resetar minha senha no aplicativo?",
            "Acesse Configurações > Segurança > Redefinir Senha.",
        )

        # Pergunta semanticamente equivalente com palavras diferentes -> HIT
        ans, score = sem_cache.lookup("Esqueci minha senha do app, como posso redefinir?")
        self.assertIsNotNone(ans)
        self.assertGreaterEqual(score, 0.80)

        # Pergunta com número/ano diferente NÃO deve dar falso positivo
        sem_cache.store("Qual o faturamento em 2024?", "R$ 10 milhões")
        ans_year, _ = sem_cache.lookup("Qual o faturamento em 2025?")
        self.assertIsNone(ans_year)

    def test_5_context_trimmer_caps_history_and_prunes_tool_outputs(self) -> None:
        trimmer = ContextTrimmer(window_size=3, summary_fixed_tokens=100)
        history = [
            ConversationMessage("user", "Msg 1", tokens=500),
            ConversationMessage("assistant", "Msg 2", tokens=500),
            ConversationMessage("user", "Msg 3", tokens=500),
            ConversationMessage("tool", "Giant JSON", tokens=3000, is_tool_output=True),
            ConversationMessage("user", "Msg 5", tokens=200),
            ConversationMessage("assistant", "Msg 6", tokens=200),
        ]
        raw_tokens, trimmed_tokens = trimmer.trim(history)
        self.assertEqual(raw_tokens, 4900)
        # 100 (resumo das 3 antigas) + 120 (tool podada) + 200 + 200 = 620 tokens
        self.assertEqual(trimmed_tokens, 620)
        self.assertLess(trimmed_tokens, raw_tokens * 0.2)

    def test_6_smaller_model_distillation_and_4bit_quantization(self) -> None:
        report = evaluate_model_distillation_and_quantization(
            teacher_params_b=70.0, student_params_b=8.0, quantization_bits=4
        )
        self.assertGreater(report.vram_reduction_pct, 90.0)
        self.assertGreaterEqual(report.retained_accuracy_pct, 99.0)
        self.assertGreater(report.cost_reduction_pct, 95.0)

    def test_unified_gateway_achieves_over_85_percent_savings(self) -> None:
        gateway = AICostOptimizationGateway()
        history = [ConversationMessage("user", f"Turn {i}", tokens=400) for i in range(10)]

        for _ in range(10):
            gateway.process_online_request(
                query="Como faço para resetar minha senha no aplicativo?",
                system_prompt="System prompt padrão de suporte",
                tool_schemas='{"tools": ["reset"]}',
                prefix_tokens=2048,
                history=history,
                query_tokens=50,
                expected_output_tokens=100,
            )

        self.assertGreater(gateway.metrics.savings_percentage, 85.0)
        self.assertEqual(gateway.metrics.semantic_cache_hits, 9)


if __name__ == "__main__":
    unittest.main()
