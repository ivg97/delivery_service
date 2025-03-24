from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI


async def startup():
    print("Подключение к БД...")


async def shutdown():
    print("Закрытие БД...")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()

app = FastAPI(
    title='Delivery Service',
    lifespan=lifespan,
)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=5000,
        reload=True
    )
