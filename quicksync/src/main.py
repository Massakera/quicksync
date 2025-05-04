from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .api.router import router as contacts_router

load_dotenv()

app = FastAPI(
    title="QuickSync",
    description="A tool that syncs contacts from MockAPI to Mailchimp",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to QuickSync API",
        "docs": "/docs",
        "sync_endpoint": "/contacts/sync"
    }