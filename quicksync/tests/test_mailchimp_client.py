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
    
    mock_client.lists.get_all_lists.return_value = {
        "lists": [
            {"id": "test_list_id", "name": "Enzo Massaki Ito"},
            {"id": "other_list_id", "name": "Other List"},
        ]
    }
    
    list_id = await client.get_or_create_list()
    
    assert list_id == "test_list_id"
    assert client.list_id == "test_list_id"
    mock_client.lists.create_list.assert_not_called()


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