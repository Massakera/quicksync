from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
from pathlib import Path

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

static_dir = os.path.join(Path(__file__).parent.parent.parent, "static")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/", include_in_schema=False)
async def root():
    static_index = os.path.join(static_dir, "index.html")
    if os.path.exists(static_index):
        return FileResponse(static_index)
    return {
        "message": "Welcome to QuickSync API. Static file directory might be misconfigured.",
        "docs": "/docs",
        "sync_endpoint": "/contacts/sync"
    }