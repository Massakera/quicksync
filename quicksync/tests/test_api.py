import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from quicksync.src.main import app
from quicksync.src.models.contact import Contact, SyncResponse


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def mock_sync_service():
    mock_contacts = [
        Contact(firstName="Amelia", lastName="Earhart", email="amelia_earhart@gmail.com"),
    ]
    
    mock_response = SyncResponse(
        syncedContacts=len(mock_contacts),
        contacts=mock_contacts,
    )
    
    mock_service = AsyncMock()
    mock_service.sync_contacts.return_value = mock_response
    
    with patch("quicksync.src.api.router.SyncService", return_value=mock_service):
        yield mock_service


def test_sync_contacts(test_client, mock_sync_service):
    response = test_client.get("/contacts/sync")
    
    assert response.status_code == 200
    
    response_json = response.json()
    assert response_json["syncedContacts"] == 1
    assert len(response_json["contacts"]) == 1
    assert response_json["contacts"][0]["firstName"] == "Amelia"
    assert response_json["contacts"][0]["email"] == "amelia_earhart@gmail.com"
    
    mock_sync_service.sync_contacts.assert_called_once()