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


@router.get('/get_types',
            response_model=ListTypePackage)
async def get_type_package(
        db_session: Session = Depends(get_session),
):
    """Doc"""
    repository = TypePackageRepository(db_session)
    types = await repository.get_all()
    return types


@router.get('/get_packages',
            response_model=ListPackage)
async def get_packages(
        session_id: str,
        db_session: Session = Depends(get_session),
):
    """Doc"""
    repository = PackageRepository(db_session)
    packages = await repository.get_packages(session_id)
    return packages


@router.get('get_by_id',
            response_model=Package)
async def get_package_by_id(
        package_id: str,
        db_session: Session = Depends(get_session),
):
    """Doc"""
    repository = PackageRepository(db_session)
    package = await repository.get_by_id(package_id)
    return package
