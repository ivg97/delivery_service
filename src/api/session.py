import uuid

from fastapi import APIRouter, Cookie, HTTPException, Depends
from fastapi.openapi.models import Response

from delivery_service.src.schemas.package import PackageResponse, CreatePackage
from delivery_service.src.tools.session import AsyncSessionManager, get_current_session, get_manager

router = APIRouter(tags=['session'])


@router.post('/create')
async def create_session(
        manager: AsyncSessionManager = Depends(get_manager())
):
    session_id = await manager.create_session()
    return session_id
