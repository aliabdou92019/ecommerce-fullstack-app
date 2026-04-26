from fastapi import FastAPI
from database import engine  , Base
from models import *
from routers.users import router as users_router
from routers.products import router as products_router
app = FastAPI(title="E-Commerce app")
Base.metadata.create_all(bind=engine)
app.include_router(users_router)
app.include_router(products_router)

@app.get("/")
def root():
    return {"message": "Hello World!"}
