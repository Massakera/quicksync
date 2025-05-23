import os
import logging

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from typing import Dict, List, Optional

from ..models.contact import Contact


class MailchimpClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        server_prefix: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("MAILCHIMP_API_KEY")
        self.server_prefix = server_prefix or os.getenv("MAILCHIMP_SERVER_PREFIX")
        self.list_name = "Enzo Massaki Ito"
        
        if not self.api_key or not self.server_prefix:
            raise ValueError("Mailchimp API key and server prefix are required")
        
        self.client = MailchimpMarketing.Client()
        self.client.set_config({
            "api_key": self.api_key,
            "server": self.server_prefix
        })
        
        self.list_id = None
    
    async def get_or_create_list(self) -> str:
        try:
            lists = self.client.lists.get_all_lists(fields=["lists.id", "lists.name"])
            found_list_id = None
            for list_info in lists["lists"]:
                if list_info["name"] == self.list_name:
                    found_list_id = list_info["id"]
                    break 
            
            if found_list_id:
                try:
                    self.client.lists.delete_list(found_list_id)
                except ApiClientError as delete_error:
                    logging.warning(f"Failed to delete list {found_list_id}: {delete_error}")
        except ApiClientError as get_error:
            logging.warning(f"Error during list check/delete phase: {get_error}. Proceeding to create.")
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
            error_details = f"Status Code: {getattr(error, 'status_code', 'N/A')}, Body: {getattr(error, 'text', 'N/A')}"
            logging.error(f"Failed to create Mailchimp list: {error_details}")
            raise ValueError(f"Failed to create Mailchimp list: {error_details}")
    
    async def add_members(self, contacts: List[Contact]) -> List[Dict]:
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
                    logging.error(f"Error adding {contact.email}: {str(error)}")
                
        return results