# QuickSync

A tool that syncs contacts from MockAPI to Mailchimp.

## Features

- Fetches contacts from MockAPI (https://challenge.trio.dev/api/v1/contacts)
- Creates a new list in Mailchimp with the name "Enzo Massaki Ito"
- Syncs contacts to the Mailchimp list
- Provides a simple API endpoint to trigger the sync process

## Requirements

- Python 3.12+
- uv (Python package installer and environment manager)
- Mailchimp API key

## Installation

```bash
uv venv
source .venv/bin/activate 
uv pip install -e .
```

## Configuration

Create a `.env` file in the project root with the following variables:

```
MAILCHIMP_API_KEY=your_mailchimp_api_key
MAILCHIMP_SERVER_PREFIX=your_mailchimp_server_prefix
```

## Usage

Start the server:

```bash
uvicorn quicksync.src.main:app --reload
```

To sync contacts, make a GET request to `/contacts/sync`:

```bash
curl http://localhost:8000/contacts/sync
```

Response format:

```json
{
  "syncedContacts": 1,
  "contacts": [
    {
      "firstName": "Amelia",
      "lastName": "Earhart",
      "email": "amelia_earhart@gmail.com"
    }
  ]
}
```

## Testing

Run tests with pytest:

```bash
pytest
```