import uuid

from fastapi import APIRouter, Cookie, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from delivery_service.src.db import get_session
from src.scheduler.delivery_calculation import Calculate

router = APIRouter(tags=['calculations'])


@router.post('/delivery')
async def delivery_package(
        db_session: AsyncSession = Depends(get_session)
) -> str:
    """Doc"""
    cl = Calculate()
    await cl.calculate_delivery(db_session)
    return 'ok'
