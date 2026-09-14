"""Processador Serverless de Eventos de CDC (Change Data Capture).

Consome eventos capturados pelo DynamoDB Streams via EventBridge e SQS,
deserializa as imagens (OldImage e NewImage), identifica mutações de dados
(deltas), aplica idempotência e reporta falhas parciais em lote (Batch Item Failures).
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def unmarshal_dynamodb_type(val: Dict[str, Any]) -> Any:
    """Converte a representação de tipo do DynamoDB (ex: {"S": "foo"}, {"N": "10"}) em tipos nativos Python."""
    if not isinstance(val, dict):
        return val
    if "S" in val:
        return val["S"]
    if "N" in val:
        num_str = val["N"]
        return float(num_str) if "." in num_str else int(num_str)
    if "BOOL" in val:
        return val["BOOL"]
    if "NULL" in val:
        return None
    if "M" in val:
        return {k: unmarshal_dynamodb_type(v) for k, v in val["M"].items()}
    if "L" in val:
        return [unmarshal_dynamodb_type(item) for item in val["L"]]
    if "SS" in val:
        return set(val["SS"])
    if "NS" in val:
        return {float(x) if "." in x else int(x) for x in val["NS"]}
    return val


def unmarshal_dynamodb_image(image_dict: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Deserializa um dicionário completo de atributos DynamoDB para um dicionário Python limpo."""
    if not image_dict or not isinstance(image_dict, dict):
        return {}
    return {k: unmarshal_dynamodb_type(v) for k, v in image_dict.items()}


def compute_attribute_deltas(
    old_image: Dict[str, Any], new_image: Dict[str, Any]
) -> Dict[str, Dict[str, Any]]:
    """Calcula a diferença (delta) campo a campo entre o estado anterior e o novo estado."""
    deltas: Dict[str, Dict[str, Any]] = {}
    all_keys = set(old_image.keys()).union(set(new_image.keys()))

    for key in all_keys:
        old_val = old_image.get(key)
        new_val = new_image.get(key)
        if old_val != new_val:
            deltas[key] = {"old": old_val, "new": new_val}
    return deltas


class IdempotencyManager:
    """Simulador de controle de idempotência em memória.

    Em produção, utiliza-se uma tabela DynamoDB de idempotência com TTL
    ou uma chave com SETNX no ElastiCache Redis.
    """

    def __init__(self) -> None:
        self._processed_events: set[str] = set()

    def is_duplicate(self, idempotency_key: str) -> bool:
        return idempotency_key in self._processed_events

    def mark_processed(self, idempotency_key: str) -> None:
        self._processed_events.add(idempotency_key)


idempotency_manager = IdempotencyManager()


def process_cdc_event(cdc_detail: Dict[str, Any]) -> None:
    """Executa as ações de downstream com base no tipo de operação CDC (INSERT, MODIFY, REMOVE)."""
    event_name = cdc_detail.get("eventName")
    dynamo_record = cdc_detail.get("dynamodb", {})

    sequence_number = dynamo_record.get("SequenceNumber", "UNKNOWN_SEQ")
    keys = unmarshal_dynamodb_image(dynamo_record.get("Keys", {}))
    order_id = keys.get("orderId", "N/A")

    # Chave composta de idempotência: Entidade + Sequência única do Transaction Log
    idempotency_key = f"{order_id}#{sequence_number}"

    if idempotency_manager.is_duplicate(idempotency_key):
        logger.warning(
            "[IDEMPOTENCY] Evento duplicado ignorado: %s", idempotency_key
        )
        return

    old_image = unmarshal_dynamodb_image(dynamo_record.get("OldImage"))
    new_image = unmarshal_dynamodb_image(dynamo_record.get("NewImage"))

    if event_name == "INSERT":
        logger.info(
            "[CDC INSERT] Novo registro criado: Pedido %s | Valor: R$ %s",
            order_id,
            new_image.get("totalAmount"),
        )
        # Exemplo Downstream: Indexar no OpenSearch ou alimentar Data Warehouse

    elif event_name == "MODIFY":
        deltas = compute_attribute_deltas(old_image, new_image)
        logger.info(
            "[CDC MODIFY] Pedido %s alterado. Deltas detectados: %s",
            order_id,
            deltas,
        )
        # Exemplo Downstream: Se 'status' mudou, invalidar cache Redis e notificar cliente

    elif event_name == "REMOVE":
        logger.info(
            "[CDC REMOVE] Pedido %s removido. Estado final antes da exclusao: %s",
            order_id,
            old_image,
        )
        # Exemplo Downstream: Soft-delete no Data Lake ou purga de cache

    else:
        logger.info("[CDC UNKNOWN] Tipo de evento desconhecido: %s", event_name)

    idempotency_manager.mark_processed(idempotency_key)


def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Handler principal acionado pelo gatilho SQS.

    Suporta 'ReportBatchItemFailures': se uma mensagem falhar, apenas o seu
    messageId é retornado, evitando o reprocessamento desnecessário do lote inteiro.
    """
    records: List[Dict[str, Any]] = event.get("Records", [])
    batch_item_failures: List[Dict[str, str]] = []

    for record in records:
        message_id = record.get("messageId", "")
        try:
            body_str = record.get("body", "{}")
            body_json = json.loads(body_str)

            # Extração da mensagem vinda do EventBridge Bus
            detail = body_json.get("detail", {})
            if not detail and "eventName" in body_json:
                # Compatibilidade caso o evento venha direto sem encapsulamento EventBridge
                detail = body_json

            process_cdc_event(detail)

        except Exception as err:
            logger.error(
                "[ERROR] Falha no processamento da mensagem SQS %s: %s",
                message_id,
                err,
                exc_info=True,
            )
            # Adiciona identificador para retentativa seletiva
            batch_item_failures.append({"itemIdentifier": message_id})

    return {"batchItemFailures": batch_item_failures}


if __name__ == "__main__":
    import pathlib

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    sample_file = pathlib.Path(__file__).parent / "cdc_payload.json"

    if sample_file.exists():
        print(f"--- Carregando payload de teste: {sample_file.name} ---")
        with open(sample_file, "r", encoding="utf-8") as f:
            test_event = json.load(f)

        result = lambda_handler(test_event)
        print("\n--- Resultado da Execução do Lambda ---")
        print(json.dumps(result, indent=2))
        print("--- Processamento concluído com sucesso! ---")
