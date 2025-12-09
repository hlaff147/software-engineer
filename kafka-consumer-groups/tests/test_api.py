"""
Integration tests for the FastAPI endpoints.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.asyncio
async def test_root_endpoint(async_client):
    """Test the root health check endpoint."""
    response = await async_client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"


@pytest.mark.asyncio
async def test_consumers_status_endpoint(async_client):
    """Test getting consumer status."""
    response = await async_client.get("/consumers/status")
    
    assert response.status_code == 200
    data = response.json()
    
    # Both consumer groups should be present
    assert "consumer_group_a" in data
    assert "consumer_group_b" in data
    
    # Verify structure
    assert data["consumer_group_a"]["group_id"] == "group-A"
    assert data["consumer_group_b"]["group_id"] == "group-B"


@pytest.mark.asyncio
async def test_reset_consumers_endpoint(async_client):
    """Test resetting both consumers."""
    response = await async_client.post("/consumers/reset")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "reset"
