import uuid

from fastapi import APIRouter, Cookie, HTTPException, Depends
from fastapi.openapi.models import Response
from sqlalchemy.orm import Session

from delivery_service.src.database.repositories.package import \
    TypePackageRepository, PackageRepository
from delivery_service.src.db import get_session
from delivery_service.src.schemas.package import PackageResponse, \
    CreatePackage, TypePackage, ListTypePackage, ListPackage, Package
from delivery_service.src.tools.session import AsyncSessionManager, \
    get_current_session, get_manager

router = APIRouter(tags=['calculations'])


@router.post('/delivery')
async def delivery_package(
        db_session: Session = Depends(get_session())
) -> dict:
    """Doc"""

    return {'status': 'ok'}
