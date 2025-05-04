#!/usr/bin/env python
import asyncio
import json
import os
import sys
import httpx
from dotenv import load_dotenv
import mailchimp_marketing
from mailchimp_marketing.api_client import ApiClientError

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Load environment variables
load_dotenv()

class Contact:
    def __init__(self, firstName, lastName, email):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
    
    def to_dict(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email
        }

class MockAPIClient:
    def __init__(self, base_url="https://challenge.trio.dev/api/v1"):
        self.base_url = base_url
        self.contacts_url = f"{base_url}/contacts"
    
    async def get_contacts(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.contacts_url)
            response.raise_for_status()
            
            contacts_data = response.json()
            return [
                Contact(
                    firstName=contact.get("firstName", ""),
                    lastName=contact.get("lastName", ""),
                    email=contact.get("email", "")
                )
                for contact in contacts_data
            ]

class MailchimpClient:
    def __init__(self):
        self.api_key = os.environ.get("MAILCHIMP_API_KEY")
        self.server_prefix = os.environ.get("MAILCHIMP_SERVER_PREFIX")
        self.list_name = "Enzo Massaki Ito"
        
        if not self.api_key or not self.server_prefix:
            raise ValueError("Mailchimp API key and server prefix are required")
        
        self.client = mailchimp_marketing.Client()
        self.client.set_config({
            "api_key": self.api_key,
            "server": self.server_prefix
        })
        
        self.list_id = None
    
    async def get_or_create_list(self):
        if self.list_id:
            return self.list_id
        
        try:
            lists = self.client.lists.get_all_lists()
            for list_info in lists["lists"]:
                if list_info["name"] == self.list_name:
                    self.list_id = list_info["id"]
                    return self.list_id
        except ApiClientError:
            pass
        
        try:
            contact = {
                "company": "QuickSync",
                "address1": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip": "10001",
                "country": "US"
            }
            
            list_info = self.client.lists.create_list({
                "name": self.list_name,
                "contact": contact,
                "permission_reminder": "You're receiving this email because you signed up for QuickSync.",
                "email_type_option": True,
                "campaign_defaults": {
                    "from_name": "QuickSync",
                    "from_email": "noreply@quicksync.com",
                    "subject": "QuickSync Update",
                    "language": "EN_US"
                }
            })
            
            self.list_id = list_info["id"]
            return self.list_id
        except ApiClientError as error:
            raise ValueError(f"Failed to create Mailchimp list: {error}")
    
    async def add_members(self, contacts):
        if not self.list_id:
            await self.get_or_create_list()
            
        results = []
        for contact in contacts:
            try:
                result = self.client.lists.add_list_member(
                    self.list_id,
                    {
                        "email_address": contact.email,
                        "status": "subscribed",
                        "merge_fields": {
                            "FNAME": contact.firstName,
                            "LNAME": contact.lastName
                        }
                    }
                )
                results.append(result)
            except ApiClientError as error:
                if "Member Exists" in str(error):
                    results.append({"status": "subscribed", "email_address": contact.email})
                else:
                    print(f"Error adding {contact.email}: {str(error)}", file=sys.stderr)
                
        return results

class SyncService:
    def __init__(self):
        self.mockapi_client = MockAPIClient()
        self.mailchimp_client = MailchimpClient()
    
    async def sync_contacts(self):
        contacts = await self.mockapi_client.get_contacts()
        await self.mailchimp_client.get_or_create_list()
        await self.mailchimp_client.add_members(contacts)
        
        return {
            "syncedContacts": len(contacts),
            "contacts": [contact.to_dict() for contact in contacts]
        }

async def main():
    sync_service = SyncService()
    result = await sync_service.sync_contacts()
    print(json.dumps(result))

if __name__ == "__main__":
    asyncio.run(main())