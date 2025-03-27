import uuid

from fastapi import Cookie

from delivery_service.src.tools.cache import SessionCache


class AsyncSessionManager:
    def __init__(self):
        self.redis: SessionCache = SessionCache()

    async def create_session(self) -> str:
        """Создает новую сессию"""
        session_id = str(uuid.uuid4())
        await self.redis.set(session_id)
        return session_id

    async def validate_session(self, session_id: str) -> bool:
        """Проверяет валидность сессии"""
        return await self.redis.validate(session_id)

    async def delete_session(self, session_id: str) -> str:
        """Удаляет сессию"""
        if await self.redis.validate(session_id):
            await self.redis.delete(session_id)
            return session_id


async def get_current_session(session_id: str = Cookie(None, alias="delivery_session")):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id
