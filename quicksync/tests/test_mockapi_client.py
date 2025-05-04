import pytest
from unittest.mock import AsyncMock, patch

from quicksync.src.clients.mockapi import MockAPIClient


@pytest.mark.asyncio
async def test_get_contacts():
    mock_contacts = [
        {"firstName": "Amelia", "lastName": "Earhart", "email": "amelia_earhart@gmail.com"},
        {"firstName": "Marie", "lastName": "Curie", "email": "marie_curie@gmail.com"},
    ]
    
    mock_response = AsyncMock()
    mock_response.json.return_value = mock_contacts
    mock_response.raise_for_status = AsyncMock()
    
    with patch("httpx.AsyncClient.get", return_value=mock_response):
        client = MockAPIClient()
        contacts = await client.get_contacts()
        
        assert len(contacts) == 2
        assert contacts[0].firstName == "Amelia"
        assert contacts[0].lastName == "Earhart"
        assert contacts[0].email == "amelia_earhart@gmail.com"