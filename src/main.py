from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from delivery_service.src.api.package import router as package_router
from delivery_service.src.api.session import router as session_router


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

app.include_router(package_router, prefix='/package')
app.include_router(session_router, prefix='/session')


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=5000,
        reload=True
    )
