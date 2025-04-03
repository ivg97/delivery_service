import json
import logging
from decimal import Decimal

import aiohttp
import aioredis

from delivery_service.src.config import settings
from delivery_service.src.database.repositories.package import \
    PackageRepository
from delivery_service.src.db import get_session
from src.tools.cache import USDCache

logger = logging.getLogger(__name__)


class Calculate:

    def __init__(self):
        self.SOURCE_USD = settings.SOURCE_USD

    async def get_usd_rate(self) -> float:
        """Получение и кеширование курса USD из ЦБ РФ"""
        cache = USDCache()
        cached_rate = await cache.get()

        if cached_rate:
            return float(cached_rate)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.SOURCE_USD) as response:
                    response.raise_for_status()
                    text = await response.text()
                    data = json.loads(text)
                    usd = float(data["Valute"]["USD"]["Value"])

                    # data = await response.json()
                    # usd = data['Valute']['USD']['Value']
                    print(usd)
                await cache.set(usd)
                return usd
        except aiohttp.ClientError as e:
            logger.error(f'Ошибка при получении USD: {str(e)}')
        except Exception as e:
            logger.error(f'Неизвестная ошибка при получении USD: {str(e)}')
        return 0.0

    async def calculate_delivery(self, session):
        try:
            db_session = get_session()
            repository = PackageRepository(db_session)

            usd_rate = await self.get_usd_rate()
            if not usd_rate:
                logger.error('Ошибка получения USD!')
                return
            usd_rate_decimal = Decimal(usd_rate)

            packages = await repository.get_all(session)
            updates = []
            for package in packages:
                try:
                    delivery_calc = ((int(package.weight) * 0.5
                                     + package.delivery_price * 0.01)
                                     * usd_rate)
                except ValueError:
                    delivery_calc = 0
                updates.append(
                    (package.id, delivery_calc)
                )
            await repository.update_calc_bulk(session, updates)
        except Exception as e:
            logger.error(f'Ошибка в расчете стоимости доставки! {e}')

