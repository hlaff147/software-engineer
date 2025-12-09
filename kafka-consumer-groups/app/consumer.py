"""Kafka Consumer Service."""
import logging
import asyncio
from dataclasses import dataclass, field
from typing import List, Optional, Set
from datetime import datetime
from aiokafka import AIOKafkaConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ConsumedMessage:
    """Represents a consumed message."""
    offset: int
    partition: int
    value: str
    key: Optional[str]
    timestamp: datetime
    acknowledged: bool = False
    
    def to_dict(self):
        return {
            "offset": self.offset,
            "partition": self.partition,
            "value": self.value,
            "key": self.key,
            "timestamp": self.timestamp.isoformat(),
            "acknowledged": self.acknowledged
        }


class KafkaConsumerService:
    """
    Async Kafka Consumer service with manual acknowledgment tracking.
    
    This consumer tracks which messages have been received and acknowledged,
    allowing us to demonstrate that different consumer groups maintain
    independent offset tracking.
    """
    
    def __init__(
        self, 
        bootstrap_servers: str,
        topic: str,
        group_id: str,
        consumer_name: str
    ):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer_name = consumer_name
        
        self._consumer: Optional[AIOKafkaConsumer] = None
        self._messages: List[ConsumedMessage] = []
        self._acknowledged_offsets: Set[int] = set()
        self._running = False
        self._task: Optional[asyncio.Task] = None
    
    @property
    def is_running(self) -> bool:
        return self._running
    
    @property
    def messages_received(self) -> List[dict]:
        return [msg.to_dict() for msg in self._messages]
    
    @property
    def messages_acknowledged(self) -> int:
        return len(self._acknowledged_offsets)
    
    async def start(self):
        """Start consuming messages."""
        self._consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=True,  # Auto commit for simplicity
            value_deserializer=lambda v: v.decode('utf-8'),
            key_deserializer=lambda k: k.decode('utf-8') if k else None
        )
        
        await self._consumer.start()
        self._running = True
        
        logger.info(
            f"[{self.consumer_name}] Started with group_id='{self.group_id}', "
            f"listening to topic '{self.topic}'"
        )
        
        try:
            async for msg in self._consumer:
                consumed_msg = ConsumedMessage(
                    offset=msg.offset,
                    partition=msg.partition,
                    value=msg.value,
                    key=msg.key,
                    timestamp=datetime.fromtimestamp(msg.timestamp / 1000)
                )
                self._messages.append(consumed_msg)
                
                logger.info(
                    f"[{self.consumer_name}] Received message: "
                    f"offset={msg.offset}, value='{msg.value}'"
                )
        except asyncio.CancelledError:
            logger.info(f"[{self.consumer_name}] Consumer loop cancelled")
        finally:
            self._running = False
    
    async def stop(self):
        """Stop consuming messages."""
        self._running = False
        if self._consumer:
            await self._consumer.stop()
            logger.info(f"[{self.consumer_name}] Stopped")
    
    def acknowledge_message(self, offset: int) -> bool:
        """
        Manually acknowledge a message by offset.
        
        This is for demonstration purposes - in real Kafka, commits
        are handled differently. This shows that acknowledging in
        one consumer group doesn't affect the other.
        """
        for msg in self._messages:
            if msg.offset == offset:
                msg.acknowledged = True
                self._acknowledged_offsets.add(offset)
                logger.info(
                    f"[{self.consumer_name}] Acknowledged message at offset {offset}"
                )
                return True
        return False
    
    def reset(self):
        """Reset message tracking for fresh testing."""
        self._messages.clear()
        self._acknowledged_offsets.clear()
        logger.info(f"[{self.consumer_name}] Reset message tracking")
