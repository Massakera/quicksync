import pytest
from unittest.mock import MagicMock, patch

from quicksync.src.clients.mailchimp import MailchimpClient
from quicksync.src.models.contact import Contact


@pytest.fixture
def mock_mailchimp_client():
    with patch("mailchimp_marketing.Client") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        client = MailchimpClient(
            api_key="test_api_key",
            server_prefix="test_server"
        )
        
        yield client, mock_client


@pytest.mark.asyncio
async def test_get_or_create_list_existing(mock_mailchimp_client):
    client, mock_client = mock_mailchimp_client
    
    existing_list_id = "test_list_id_to_be_deleted"
    newly_created_list_id = "newly_created_list_id_after_delete"

    mock_client.lists.get_all_lists.return_value = {
        "lists": [
            {"id": existing_list_id, "name": "Enzo Massaki Ito"},
            {"id": "other_list_id", "name": "Other List"},
        ]
    }
    
    mock_client.lists.delete_list = MagicMock()
    
    mock_client.lists.create_list.return_value = {"id": newly_created_list_id}
    
    list_id_from_method = await client.get_or_create_list()
    
    mock_client.lists.get_all_lists.assert_called_once()
    mock_client.lists.delete_list.assert_called_once_with(existing_list_id)
    mock_client.lists.create_list.assert_called_once() 
    
    assert list_id_from_method == newly_created_list_id
    assert client.list_id == newly_created_list_id


@pytest.mark.asyncio
async def test_get_or_create_list_new(mock_mailchimp_client):
    client, mock_client = mock_mailchimp_client
    
    mock_client.lists.get_all_lists.return_value = {
        "lists": [
            {"id": "other_list_id", "name": "Other List"},
        ]
    }
    
    mock_client.lists.create_list.return_value = {"id": "new_list_id"}
    
    list_id = await client.get_or_create_list()
    
    assert list_id == "new_list_id"
    assert client.list_id == "new_list_id"
    mock_client.lists.create_list.assert_called_once()