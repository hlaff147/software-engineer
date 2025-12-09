"""
Unit tests for Kafka Producer Service.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.producer import KafkaProducerService, ProduceResult


@pytest.mark.asyncio
async def test_producer_start():
    """Test that producer starts correctly."""
    with patch('app.producer.AIOKafkaProducer') as mock_producer_class:
        mock_instance = AsyncMock()
        mock_producer_class.return_value = mock_instance
        
        producer = KafkaProducerService("localhost:9092")
        await producer.start()
        
        mock_producer_class.assert_called_once()
        mock_instance.start.assert_called_once()


@pytest.mark.asyncio
async def test_producer_stop():
    """Test that producer stops correctly."""
    with patch('app.producer.AIOKafkaProducer') as mock_producer_class:
        mock_instance = AsyncMock()
        mock_producer_class.return_value = mock_instance
        
        producer = KafkaProducerService("localhost:9092")
        await producer.start()
        await producer.stop()
        
        mock_instance.stop.assert_called_once()


@pytest.mark.asyncio
async def test_producer_send_message():
    """Test sending a message."""
    with patch('app.producer.AIOKafkaProducer') as mock_producer_class:
        mock_instance = AsyncMock()
        
        # Mock the send result
        send_result = MagicMock()
        send_result.topic = "demo-topic"
        send_result.partition = 0
        send_result.offset = 42
        mock_instance.send_and_wait = AsyncMock(return_value=send_result)
        
        mock_producer_class.return_value = mock_instance
        
        producer = KafkaProducerService("localhost:9092")
        await producer.start()
        
        result = await producer.send_message(
            topic="demo-topic",
            value="test message",
            key="test-key"
        )
        
        assert isinstance(result, ProduceResult)
        assert result.topic == "demo-topic"
        assert result.partition == 0
        assert result.offset == 42


@pytest.mark.asyncio
async def test_producer_send_without_start():
    """Test that sending without starting raises an error."""
    producer = KafkaProducerService("localhost:9092")
    
    with pytest.raises(RuntimeError, match="Producer not started"):
        await producer.send_message(topic="demo-topic", value="test")
