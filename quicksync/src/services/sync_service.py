from ..clients.mockapi import MockAPIClient
from ..clients.mailchimp import MailchimpClient
from ..models.contact import SyncResponse


class SyncService:
    def __init__(
        self,
        mockapi_client: MockAPIClient = None,
        mailchimp_client: MailchimpClient = None,
    ):
        self.mockapi_client = mockapi_client or MockAPIClient()
        self.mailchimp_client = mailchimp_client or MailchimpClient()
    
    async def sync_contacts(self) -> SyncResponse:
        contacts = await self.mockapi_client.get_contacts()
        await self.mailchimp_client.get_or_create_list()
        await self.mailchimp_client.add_members(contacts)
        
        return SyncResponse(
            syncedContacts=len(contacts),
            contacts=contacts,
        )