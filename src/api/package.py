import uuid

from fastapi import APIRouter, Cookie, HTTPException, Depends
from fastapi.openapi.models import Response

from delivery_service.src.schemas.package import PackageResponse, CreatePackage
from delivery_service.src.tools.session import AsyncSessionManager, get_current_session

router = APIRouter(tags=['package'])


@router.post('/register',
             response_model=PackageResponse)
async def register_package(
    package: CreatePackage,
    session_id: str = Depends(get_current_session),
):
    """Doc"""
    if not await AsyncSessionManager.validate_session(session_id):
        raise HTTPException(status_code=401, detail='Invalid session')

    order_id = str(uuid.uuid4())
    print(order_id, session_id)



# @router.get()
# async def get_type_package():
#     '''Doc'''
#     pass
#
# @router.get()
# async def get_packages():
#     pass
#
#
# @router.get()
# async def get_package_by_id():
#     '''Doc'''
#     pass
