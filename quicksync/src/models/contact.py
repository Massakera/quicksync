from pydantic import BaseModel, EmailStr


class Contact(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr


class SyncResponse(BaseModel):
    syncedContacts: int
    contacts: list[Contact]