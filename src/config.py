import aioredis
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # TIME_DELIVERY_CALCULATION: int = 300  #
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379

    SOURCE_USD: str = 'www.cbr-xml-daily.ru/daily_json.js'

    @property
    def db_url(self):
        return f'mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASS}@' \
               f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

    @property
    def create_redis_client(self) -> aioredis.Redis:
        redis_client = aioredis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
        )
        return redis_client


settings = Settings()
