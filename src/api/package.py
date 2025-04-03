import uuid
from typing import Optional, List

from fastapi import APIRouter, Cookie, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from delivery_service.src.database.repositories.package import \
    TypePackageRepository, PackageRepository
from delivery_service.src.db import get_session
from delivery_service.src.schemas.package import PackageResponse, \
    CreatePackage, ListTypePackage, ListPackage, Package
from delivery_service.src.tools.session import AsyncSessionManager, get_manager

router = APIRouter(tags=['package'])


@router.post('/register',
             response_model=PackageResponse)
async def register_package(
    package: CreatePackage,
    manager: AsyncSessionManager = Depends(get_manager()),
    db_session: Session = Depends(get_session)
):
    """Doc"""
    if not await manager.validate_session(package.session_id):
        raise HTTPException(status_code=401, detail='Invalid session')
    repository = PackageRepository(db_session)
    order = await repository.create(package)
    return package.to_response(package_id=order.id)


@router.get('/get_types')
async def get_type_package(
        db_session: AsyncSession = Depends(get_session),
):
    """Doc"""
    repository = TypePackageRepository(db_session)
    types = await repository.get_all()
    return types


@router.get('/get_packages')
async def get_packages(
        session_id: str,
        db_session: Session = Depends(get_session),
):
    """Doc"""
    repository = PackageRepository(db_session)
    packages = await repository.get_packages(session_id)
    return packages


@router.get('get_by_id')
async def get_package_by_id(
        session_id: str,
        package_id: int,
        db_session: Session = Depends(get_session),
):
    """Doc"""
    repository = PackageRepository(db_session)
    package = await repository.get_by_id(
        session_id=session_id,
        package_id=package_id)
    return package
