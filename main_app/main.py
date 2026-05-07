from fastapi import FastAPI
from database import engine  , Base
from models import *

from routers.users import router as users_router
from routers.categories import router as categories_router
from routers.products import router as products_router
from routers.orders import router as orders_router
from routers.shopping_cart import router as shopping_cart_router
from routers.categories import router as categories_router
import redis.asyncio as redis
import time
from fastapi import Request
from core.logging_config import logger
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(title="E-Commerce app")
#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
Instrumentator().instrument(app).expose(app)
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(orders_router)
app.include_router(shopping_cart_router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = round(time.time() - start_time, 4)

    logger.info(
        f"{request.method} "
        f"{request.url.path} "
        f"Status: {response.status_code} "
        f"Duration: {duration}s"
    )

    return response


@app.get("/")
def root():
    return {"message": "Hello World!"}


async def get_redis():
    client = redis.from_url("redis://localhost:6379")
    try:
        yield client
    finally:
        await client.close()  # in database.py
        
        


