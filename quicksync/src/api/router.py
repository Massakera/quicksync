from fastapi import APIRouter, Depends

from ..models.contact import SyncResponse
from ..services.sync_service import SyncService


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/sync", response_model=SyncResponse)
async def sync_contacts(
    sync_service: SyncService = Depends(lambda: SyncService())
) -> SyncResponse:
    return await sync_service.sync_contacts()