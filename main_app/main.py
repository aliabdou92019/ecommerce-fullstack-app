from fastapi import FastAPI
from database import engine  
from models import *
from routers import orders

app = FastAPI(title="E-Commerce app")
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "Hello World!"}
