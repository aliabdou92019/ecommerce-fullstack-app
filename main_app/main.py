from fastapi import FastAPI
from database import engine  , Base
from models import *

from routers.users import router as users_router
from routers.products import router as products_router
from routers.orders import router as orders_router
from routers.shopping_cart import router as shopping_cart_router
from routers.categories import router as categories_router

app = FastAPI(title="E-Commerce app")
#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
app.include_router(users_router)
app.include_router(products_router)
app.include_router(categories_router)
app.include_router(orders_router)
app.include_router(shopping_cart_router)

@app.get("/")
def root():
    return {"message": "Hello World!"}


async def get_redis():
    client = redis.from_url("redis://localhost:6379")
    try:
        yield client
    finally:
        await client.close()  # in database.py