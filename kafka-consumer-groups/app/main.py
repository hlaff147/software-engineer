"""
FastAPI application to demonstrate Kafka consumer group behavior.

This demo proves that consumers with different group IDs can independently
acknowledge messages - one consumer's acknowledgment doesn't affect the other.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import asyncio

from app.producer import KafkaProducerService
from app.consumer import KafkaConsumerService
from app.config import settings


class Message(BaseModel):
    content: str
    key: Optional[str] = None


class ProduceResponse(BaseModel):
    status: str
    topic: str
    partition: int
    offset: int


# Global instances
producer_service: Optional[KafkaProducerService] = None
consumer_group_a: Optional[KafkaConsumerService] = None
consumer_group_b: Optional[KafkaConsumerService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - start/stop Kafka services."""
    global producer_service, consumer_group_a, consumer_group_b
    
    # Initialize producer
    producer_service = KafkaProducerService(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
    )
    await producer_service.start()
    
    # Initialize consumers with different group IDs
    consumer_group_a = KafkaConsumerService(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        topic=settings.KAFKA_TOPIC,
        group_id="group-A",
        consumer_name="Consumer-A"
    )
    
    consumer_group_b = KafkaConsumerService(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        topic=settings.KAFKA_TOPIC,
        group_id="group-B",
        consumer_name="Consumer-B"
    )
    
    # Start consumers in background
    asyncio.create_task(consumer_group_a.start())
    asyncio.create_task(consumer_group_b.start())
    
    yield
    
    # Cleanup
    if producer_service:
        await producer_service.stop()
    if consumer_group_a:
        await consumer_group_a.stop()
    if consumer_group_b:
        await consumer_group_b.stop()


app = FastAPI(
    title="Kafka Consumer Groups Demo",
    description="Demonstrates that consumers with different group IDs can independently acknowledge messages",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "message": "Kafka Consumer Groups Demo API"
    }


@app.post("/produce", response_model=ProduceResponse)
async def produce_message(message: Message):
    """
    Produce a message to Kafka topic.
    
    This message will be received by BOTH consumers since they have different group IDs.
    """
    if not producer_service:
        raise HTTPException(status_code=503, detail="Producer not initialized")
    
    result = await producer_service.send_message(
        topic=settings.KAFKA_TOPIC,
        value=message.content,
        key=message.key
    )
    
    return ProduceResponse(
        status="sent",
        topic=result.topic,
        partition=result.partition,
        offset=result.offset
    )


@app.get("/consumers/status")
async def get_consumers_status():
    """
    Get the status of both consumers including messages received and acknowledged.
    
    This endpoint shows that each consumer receives ALL messages independently.
    """
    return {
        "consumer_group_a": {
            "group_id": "group-A",
            "messages_received": consumer_group_a.messages_received if consumer_group_a else [],
            "messages_acknowledged": consumer_group_a.messages_acknowledged if consumer_group_a else 0,
            "is_running": consumer_group_a.is_running if consumer_group_a else False
        },
        "consumer_group_b": {
            "group_id": "group-B",
            "messages_received": consumer_group_b.messages_received if consumer_group_b else [],
            "messages_acknowledged": consumer_group_b.messages_acknowledged if consumer_group_b else 0,
            "is_running": consumer_group_b.is_running if consumer_group_b else False
        }
    }


@app.post("/consumers/{consumer_name}/acknowledge")
async def acknowledge_message(consumer_name: str, message_offset: int):
    """
    Manually acknowledge a specific message for a consumer.
    
    This demonstrates that acknowledging for one consumer doesn't affect the other.
    """
    if consumer_name == "A":
        if not consumer_group_a:
            raise HTTPException(status_code=503, detail="Consumer A not initialized")
        consumer_group_a.acknowledge_message(message_offset)
        return {"status": "acknowledged", "consumer": "group-A", "offset": message_offset}
    elif consumer_name == "B":
        if not consumer_group_b:
            raise HTTPException(status_code=503, detail="Consumer B not initialized")
        consumer_group_b.acknowledge_message(message_offset)
        return {"status": "acknowledged", "consumer": "group-B", "offset": message_offset}
    else:
        raise HTTPException(status_code=400, detail="Invalid consumer name. Use 'A' or 'B'")


@app.post("/consumers/reset")
async def reset_consumers():
    """Reset both consumers' message tracking for fresh testing."""
    if consumer_group_a:
        consumer_group_a.reset()
    if consumer_group_b:
        consumer_group_b.reset()
    return {"status": "reset", "message": "Both consumers have been reset"}
