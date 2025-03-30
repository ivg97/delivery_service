import logging
from decimal import Decimal

import aiohttp

from delivery_service.src.config import settings
from delivery_service.src.database.repositories.package import \
    PackageRepository
from delivery_service.src.db import get_session

logger = logging.getLogger(__name__)


class Calculate:

    def __init__(self):
        self.SOURCE_USD = settings.SOURCE_USD

    async def get_usd_rate(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.SOURCE_USD) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data['Valute']['USD']['Value']
        except aiohttp.ClientError as e:
            logger.error(f'Ошибка при получении USD: {str(e)}')
        except Exception as e:
            logger.error(f'Неизвестная ошибка при получении USD: {str(e)}')
        return None

    async def calculate_delivery(self):
        try:
            db_session = await get_session()
            repository = PackageRepository(db_session)

            usd_rate = self.get_usd_rate()
            if not usd_rate:
                logger.error('Ошибка получения USD!')
                return
            usd_rate_decimal = Decimal(usd_rate)

            packages = await repository.get_all()
            updates = []
            for package in packages:
                delivery_calc = (Decimal(package.weight * 0.5
                                 + package.delivery_price * 0.01)
                                 * usd_rate_decimal)
                updates.append(
                    (package.id, delivery_calc)
                )
            await repository.update_calc_bulk(updates)
        except Exception as e:
            logger.error(f'Ошибка в расчете стоимости доставки!')
