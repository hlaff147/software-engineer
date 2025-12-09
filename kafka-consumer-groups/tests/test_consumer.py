"""
Unit tests for Kafka Consumer Service.
"""
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch

from app.consumer import KafkaConsumerService, ConsumedMessage


class TestConsumedMessage:
    """Tests for ConsumedMessage dataclass."""
    
    def test_consumed_message_creation(self):
        """Test creating a consumed message."""
        msg = ConsumedMessage(
            offset=10,
            partition=0,
            value="test message",
            key="test-key",
            timestamp=datetime(2024, 1, 1, 12, 0, 0)
        )
        
        assert msg.offset == 10
        assert msg.partition == 0
        assert msg.value == "test message"
        assert msg.key == "test-key"
        assert msg.acknowledged is False
    
    def test_consumed_message_to_dict(self):
        """Test converting consumed message to dict."""
        msg = ConsumedMessage(
            offset=10,
            partition=0,
            value="test message",
            key="test-key",
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
            acknowledged=True
        )
        
        result = msg.to_dict()
        
        assert result["offset"] == 10
        assert result["partition"] == 0
        assert result["value"] == "test message"
        assert result["key"] == "test-key"
        assert result["acknowledged"] is True
        assert "timestamp" in result


class TestKafkaConsumerService:
    """Tests for KafkaConsumerService."""
    
    def test_consumer_initialization(self):
        """Test consumer is initialized with correct properties."""
        consumer = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="test-group",
            consumer_name="Test-Consumer"
        )
        
        assert consumer.bootstrap_servers == "localhost:9092"
        assert consumer.topic == "test-topic"
        assert consumer.group_id == "test-group"
        assert consumer.consumer_name == "Test-Consumer"
        assert consumer.is_running is False
        assert consumer.messages_received == []
        assert consumer.messages_acknowledged == 0
    
    def test_acknowledge_message(self):
        """Test acknowledging a message."""
        consumer = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="test-group",
            consumer_name="Test-Consumer"
        )
        
        # Manually add a message to simulate receiving it
        msg = ConsumedMessage(
            offset=5,
            partition=0,
            value="test",
            key=None,
            timestamp=datetime.now()
        )
        consumer._messages.append(msg)
        
        # Acknowledge the message
        result = consumer.acknowledge_message(5)
        
        assert result is True
        assert consumer.messages_acknowledged == 1
        assert msg.acknowledged is True
    
    def test_acknowledge_nonexistent_message(self):
        """Test acknowledging a message that doesn't exist."""
        consumer = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="test-group",
            consumer_name="Test-Consumer"
        )
        
        result = consumer.acknowledge_message(999)
        
        assert result is False
        assert consumer.messages_acknowledged == 0
    
    def test_reset(self):
        """Test resetting the consumer state."""
        consumer = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="test-group",
            consumer_name="Test-Consumer"
        )
        
        # Add some messages
        msg = ConsumedMessage(
            offset=5,
            partition=0,
            value="test",
            key=None,
            timestamp=datetime.now()
        )
        consumer._messages.append(msg)
        consumer.acknowledge_message(5)
        
        # Reset
        consumer.reset()
        
        assert consumer.messages_received == []
        assert consumer.messages_acknowledged == 0
    
    @pytest.mark.asyncio
    async def test_consumer_stop(self):
        """Test stopping the consumer."""
        with patch('app.consumer.AIOKafkaConsumer') as mock_consumer_class:
            mock_instance = AsyncMock()
            mock_consumer_class.return_value = mock_instance
            
            consumer = KafkaConsumerService(
                bootstrap_servers="localhost:9092",
                topic="test-topic",
                group_id="test-group",
                consumer_name="Test-Consumer"
            )
            
            # Simulate that consumer was started
            consumer._consumer = mock_instance
            consumer._running = True
            
            await consumer.stop()
            
            mock_instance.stop.assert_called_once()
            assert consumer.is_running is False
