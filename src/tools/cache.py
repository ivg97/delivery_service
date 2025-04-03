import aioredis

from delivery_service.src.config import settings


class SessionCache:
    def __init__(self):
        self.cli = settings.create_redis_client

    async def set(self, session_id: str) -> str:
        """Кэширует сессию"""
        await self.cli.set(session_id, 'ok')
        return session_id

    async def check_exist(self, session_id: str) -> bool:
        """Проверяет существование сессии"""
        return await self.cli.exists(session_id) == 1

    async def delete(self, session_id: str):
        """Удаляет сессию"""
        if await self.cli.exists(session_id):
            await self.cli.delete(session_id)


class USDCache:
    def __init__(self):
        self.cli = settings.create_redis_client

    async def set(self, usd: float):
        await self.cli.set(name='usd', value=usd)

    async def get(self):
        usd = await self.cli.get('usd')
        if usd:
            return usd
