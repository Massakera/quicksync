import pytest
from unittest.mock import AsyncMock

from quicksync.src.services.sync_service import SyncService
from quicksync.src.models.contact import Contact


@pytest.mark.asyncio
async def test_sync_contacts():
    mock_contacts = [
        Contact(firstName="Amelia", lastName="Earhart", email="amelia_earhart@gmail.com"),
        Contact(firstName="Marie", lastName="Curie", email="marie_curie@gmail.com"),
    ]
    
    mock_mockapi_client = AsyncMock()
    mock_mockapi_client.get_contacts.return_value = mock_contacts
    
    mock_mailchimp_client = AsyncMock()
    mock_mailchimp_client.get_or_create_list.return_value = "test_list_id"
    mock_mailchimp_client.add_members.return_value = [
        {"id": "test_member_id_1", "status": "subscribed"},
        {"id": "test_member_id_2", "status": "subscribed"},
    ]
    
    sync_service = SyncService(
        mockapi_client=mock_mockapi_client,
        mailchimp_client=mock_mailchimp_client,
    )
    
    result = await sync_service.sync_contacts()
    
    mock_mockapi_client.get_contacts.assert_called_once()
    mock_mailchimp_client.get_or_create_list.assert_called_once()
    mock_mailchimp_client.add_members.assert_called_once_with(mock_contacts)
    
    assert result.syncedContacts == 2
    assert len(result.contacts) == 2
    assert result.contacts[0].firstName == "Amelia"
    assert result.contacts[0].email == "amelia_earhart@gmail.com"