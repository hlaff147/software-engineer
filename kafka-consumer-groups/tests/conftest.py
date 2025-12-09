"""
Pytest configuration and fixtures for Kafka consumer group tests.
"""
import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch

# Fix for pytest-asyncio
pytest_plugins = ('pytest_asyncio',)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_kafka_producer():
    """Mock Kafka producer for unit tests."""
    with patch('app.producer.AIOKafkaProducer') as mock:
        producer_instance = AsyncMock()
        producer_instance.start = AsyncMock()
        producer_instance.stop = AsyncMock()
        
        # Mock send_and_wait to return a proper result
        send_result = MagicMock()
        send_result.topic = "demo-topic"
        send_result.partition = 0
        send_result.offset = 0
        producer_instance.send_and_wait = AsyncMock(return_value=send_result)
        
        mock.return_value = producer_instance
        yield mock


@pytest.fixture
def mock_kafka_consumer():
    """Mock Kafka consumer for unit tests."""
    with patch('app.consumer.AIOKafkaConsumer') as mock:
        consumer_instance = AsyncMock()
        consumer_instance.start = AsyncMock()
        consumer_instance.stop = AsyncMock()
        
        # Make the consumer not iterate (empty)
        consumer_instance.__aiter__ = lambda self: self
        consumer_instance.__anext__ = AsyncMock(side_effect=StopAsyncIteration)
        
        mock.return_value = consumer_instance
        yield mock


@pytest.fixture
async def async_client(mock_kafka_producer, mock_kafka_consumer) -> AsyncGenerator[AsyncClient, None]:
    """Create async test client with mocked Kafka."""
    from app.main import app
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
