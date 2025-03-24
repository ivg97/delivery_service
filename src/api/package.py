from fastapi import APIRouter

router = APIRouter(tags=['package'])


@router.post()
async def register_package():
    '''Doc'''
    pass


@router.get()
async def get_type_package():
    '''Doc'''
    pass

@router.get()
async def get_packages():
    pass


@router.get()
async def get_package_by_id():
    '''Doc'''
    pass
