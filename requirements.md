#Requirements

This document outlines the requirements for the Sync tool. Please, feel free to choose the name of the tool.

### Overview

You'll be creating a tool that syncs contacts from MockAPI to Mailchimp. For this integration, you will need to get each contact's first name, last name, and email address from MockAPI and create them as new members of a new list on Mailchimp. The new list on Mailchimp should have your personal name (e.g.: Gabriel Kugel).

Contacts api: https://challenge.trio.dev/api/v1/contacts

### Requirements

The web server should have this endpoint GET /contacts/sync to trigger the integration
The /contacts/sync endpoint should return the list of synced contacts in JSON following this structure:

```json
{
    "syncedContacts": 1, // total synced contacts
    "contacts": [
        {
            "firstName": "Amelia",
            "LastName": "Earhart",
            "email" : "amelia_earhart@gmail.com",
        },
    ]
}

It should use the lastest python version with uv. Also make in a modern and simple archtecture and use unit tests to cover the tool.
```