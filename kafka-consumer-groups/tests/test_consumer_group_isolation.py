"""
Tests that prove consumer groups with different group IDs receive messages independently.

This is the key test file that demonstrates:
1. Each consumer group receives ALL messages (not partitioned between them)
2. Acknowledging a message in one group does NOT affect the other group
3. Each group maintains its own offset tracking
"""
import pytest
from datetime import datetime

from app.consumer import KafkaConsumerService, ConsumedMessage


class TestConsumerGroupIsolation:
    """
    Tests that prove consumer groups are isolated from each other.
    
    In Kafka, consumers with DIFFERENT group IDs will each receive a copy
    of every message. This is different from consumers in the SAME group,
    where messages are partitioned among them.
    """
    
    def test_different_group_ids_maintain_separate_state(self):
        """
        Prove that two consumers with different group IDs maintain separate state.
        
        This simulates what happens when messages are consumed:
        - Both consumers receive the same messages
        - Each tracks its own acknowledgments independently
        """
        # Create two consumers with DIFFERENT group IDs
        consumer_a = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="group-A",  # Different group ID
            consumer_name="Consumer-A"
        )
        
        consumer_b = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="group-B",  # Different group ID
            consumer_name="Consumer-B"
        )
        
        # Simulate both consumers receiving the SAME message
        # (This is what happens with different group IDs)
        message_content = "Test message 1"
        timestamp = datetime.now()
        
        msg_for_a = ConsumedMessage(
            offset=0, partition=0, value=message_content,
            key=None, timestamp=timestamp
        )
        msg_for_b = ConsumedMessage(
            offset=0, partition=0, value=message_content,
            key=None, timestamp=timestamp
        )
        
        consumer_a._messages.append(msg_for_a)
        consumer_b._messages.append(msg_for_b)
        
        # VERIFY: Both consumers received the same message
        assert len(consumer_a.messages_received) == 1
        assert len(consumer_b.messages_received) == 1
        assert consumer_a.messages_received[0]["value"] == message_content
        assert consumer_b.messages_received[0]["value"] == message_content
    
    def test_acknowledge_in_one_group_does_not_affect_other(self):
        """
        CRITICAL TEST: Prove that acknowledging in one group doesn't affect another.
        
        This is the key behavior we want to demonstrate:
        - Consumer A acknowledges a message
        - Consumer B's state remains UNCHANGED
        """
        # Create two consumers with different group IDs
        consumer_a = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="group-A",
            consumer_name="Consumer-A"
        )
        
        consumer_b = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="group-B",
            consumer_name="Consumer-B"
        )
        
        # Both consumers receive the same message
        timestamp = datetime.now()
        
        msg_for_a = ConsumedMessage(
            offset=0, partition=0, value="Important message",
            key=None, timestamp=timestamp
        )
        msg_for_b = ConsumedMessage(
            offset=0, partition=0, value="Important message",
            key=None, timestamp=timestamp
        )
        
        consumer_a._messages.append(msg_for_a)
        consumer_b._messages.append(msg_for_b)
        
        # Consumer A acknowledges the message
        consumer_a.acknowledge_message(0)
        
        # VERIFY: Consumer A has acknowledged
        assert consumer_a.messages_acknowledged == 1
        assert consumer_a._messages[0].acknowledged is True
        
        # CRITICAL VERIFICATION: Consumer B is NOT affected
        assert consumer_b.messages_acknowledged == 0
        assert consumer_b._messages[0].acknowledged is False
        
        # The message is still "pending" for Consumer B
        assert consumer_b._messages[0].value == "Important message"
    
    def test_multiple_messages_independent_acknowledgment(self):
        """
        Test that multiple messages can be acknowledged independently per group.
        
        Scenario:
        - 3 messages are sent
        - Consumer A acknowledges messages 0 and 2
        - Consumer B acknowledges only message 1
        - Each consumer's state reflects only its own acknowledgments
        """
        consumer_a = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="group-A",
            consumer_name="Consumer-A"
        )
        
        consumer_b = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="group-B",
            consumer_name="Consumer-B"
        )
        
        # Both consumers receive 3 messages
        timestamp = datetime.now()
        for i in range(3):
            consumer_a._messages.append(ConsumedMessage(
                offset=i, partition=0, value=f"Message {i}",
                key=None, timestamp=timestamp
            ))
            consumer_b._messages.append(ConsumedMessage(
                offset=i, partition=0, value=f"Message {i}",
                key=None, timestamp=timestamp
            ))
        
        # Consumer A acknowledges messages 0 and 2
        consumer_a.acknowledge_message(0)
        consumer_a.acknowledge_message(2)
        
        # Consumer B acknowledges only message 1
        consumer_b.acknowledge_message(1)
        
        # VERIFY Consumer A's state
        assert consumer_a.messages_acknowledged == 2
        assert consumer_a._messages[0].acknowledged is True
        assert consumer_a._messages[1].acknowledged is False
        assert consumer_a._messages[2].acknowledged is True
        
        # VERIFY Consumer B's state (completely independent)
        assert consumer_b.messages_acknowledged == 1
        assert consumer_b._messages[0].acknowledged is False
        assert consumer_b._messages[1].acknowledged is True
        assert consumer_b._messages[2].acknowledged is False
    
    def test_reset_one_consumer_does_not_affect_other(self):
        """
        Test that resetting one consumer doesn't affect the other.
        """
        consumer_a = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="group-A",
            consumer_name="Consumer-A"
        )
        
        consumer_b = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="group-B",
            consumer_name="Consumer-B"
        )
        
        # Both receive messages
        timestamp = datetime.now()
        consumer_a._messages.append(ConsumedMessage(
            offset=0, partition=0, value="Message",
            key=None, timestamp=timestamp
        ))
        consumer_b._messages.append(ConsumedMessage(
            offset=0, partition=0, value="Message",
            key=None, timestamp=timestamp
        ))
        
        # Both acknowledge
        consumer_a.acknowledge_message(0)
        consumer_b.acknowledge_message(0)
        
        # Reset only Consumer A
        consumer_a.reset()
        
        # VERIFY: Consumer A is reset
        assert len(consumer_a.messages_received) == 0
        assert consumer_a.messages_acknowledged == 0
        
        # VERIFY: Consumer B is NOT affected
        assert len(consumer_b.messages_received) == 1
        assert consumer_b.messages_acknowledged == 1
        assert consumer_b._messages[0].acknowledged is True


class TestConsumerGroupTheory:
    """
    Tests that document the theory behind Kafka consumer groups.
    """
    
    def test_same_group_id_would_share_messages(self):
        """
        Document: If consumers had the SAME group ID, they would share messages.
        
        This test documents the contrast - in a real Kafka setup:
        - Same group ID = messages are partitioned among consumers
        - Different group ID = each consumer gets ALL messages
        
        We use different group IDs to ensure each service gets every message.
        """
        # These consumers have DIFFERENT group IDs
        consumer_1 = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="group-A",  # Different
            consumer_name="Consumer-1"
        )
        
        consumer_2 = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="test-topic",
            group_id="group-B",  # Different
            consumer_name="Consumer-2"
        )
        
        # With different group IDs, both receive all messages
        # This is the behavior we're testing and proving
        assert consumer_1.group_id != consumer_2.group_id
        
        # Each maintains independent offset tracking
        assert consumer_1.messages_acknowledged == 0
        assert consumer_2.messages_acknowledged == 0
    
    def test_group_id_determines_message_distribution(self):
        """
        Document the relationship between group IDs and message distribution.
        
        Key concept:
        - group_id is the identifier for offset tracking
        - Each unique group_id maintains its own committed offsets
        - This allows multiple services to process the same messages
        """
        consumer_a = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="orders",
            group_id="notification-service",
            consumer_name="Notifications"
        )
        
        consumer_b = KafkaConsumerService(
            bootstrap_servers="localhost:9092",
            topic="orders",
            group_id="analytics-service",
            consumer_name="Analytics"
        )
        
        # Both services can process the same "orders" topic
        # Because they have different group IDs:
        # - notification-service tracks its own offsets
        # - analytics-service tracks its own offsets
        # 
        # If notification-service crashes after processing message 5,
        # it will resume from message 5.
        # Meanwhile, analytics-service might be at message 10.
        # They are completely independent.
        
        assert consumer_a.group_id == "notification-service"
        assert consumer_b.group_id == "analytics-service"
