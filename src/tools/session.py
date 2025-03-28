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
        return await self.redis.check_exist(session_id)

    async def delete_session(self, session_id: str) -> str:
        """Удаляет сессию"""
        if await self.redis.check_exist(session_id):
            await self.redis.delete(session_id)
            return session_id


def get_manager():
    return AsyncSessionManager


async def get_current_session(session_id: str | None = None):
    manager = AsyncSessionManager()
    if not session_id:
        return
    elif await manager.validate_session(session_id):
        return session_id
