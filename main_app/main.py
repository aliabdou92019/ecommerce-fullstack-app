

from fastapi import FastAPI
from database import engine  
from models import *

app = FastAPI(title="E-Commerce app")
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World!"}
