from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379

    source_usd: str = 'www.cbr-xml-daily.ru/daily_json.js'

    @property
    def db_url(self):
        return f'mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASS}@' \
               f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

    @property
    def redis_storage_url(self):
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'


settings = Settings()
