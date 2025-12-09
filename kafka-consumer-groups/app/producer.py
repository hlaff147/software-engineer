"""Kafka Producer Service."""
import logging
from dataclasses import dataclass
from typing import Optional
from aiokafka import AIOKafkaProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ProduceResult:
    """Result of producing a message."""
    topic: str
    partition: int
    offset: int


class KafkaProducerService:
    """Async Kafka Producer service."""
    
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self._producer: Optional[AIOKafkaProducer] = None
    
    async def start(self):
        """Start the producer."""
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: v.encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        await self._producer.start()
        logger.info(f"Producer started, connected to {self.bootstrap_servers}")
    
    async def stop(self):
        """Stop the producer."""
        if self._producer:
            await self._producer.stop()
            logger.info("Producer stopped")
    
    async def send_message(
        self, 
        topic: str, 
        value: str, 
        key: Optional[str] = None
    ) -> ProduceResult:
        """
        Send a message to a Kafka topic.
        
        Args:
            topic: The topic to send to
            value: The message value
            key: Optional message key
            
        Returns:
            ProduceResult with topic, partition, and offset information
        """
        if not self._producer:
            raise RuntimeError("Producer not started")
        
        result = await self._producer.send_and_wait(
            topic=topic,
            value=value,
            key=key
        )
        
        logger.info(
            f"Message sent to {topic} "
            f"[partition={result.partition}, offset={result.offset}]: {value}"
        )
        
        return ProduceResult(
            topic=result.topic,
            partition=result.partition,
            offset=result.offset
        )
