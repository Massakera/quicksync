import httpx
from typing import List

from ..models.contact import Contact


class MockAPIClient:
    def __init__(self, base_url: str = "https://challenge.trio.dev/api/v1"):
        self.base_url = base_url
        self.contacts_url = f"{base_url}/contacts"
    
    async def get_contacts(self) -> List[Contact]:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.contacts_url)
            await response.raise_for_status()
            
            contacts_data = await response.json()
            return [
                Contact(
                    firstName=contact.get("firstName", ""),
                    lastName=contact.get("lastName", ""),
                    email=contact.get("email", "")
                )
                for contact in contacts_data
            ]