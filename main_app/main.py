from fastapi import FastAPI
from database import engine  
from models import *
from routers.users import router as users_router
app = FastAPI(title="E-Commerce app")
Base.metadata.create_all(bind=engine)
app.include_router(users_router)
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World!"}
