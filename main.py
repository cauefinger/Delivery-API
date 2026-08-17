from fastapi import FastAPI
import os
from dotenv import load_dotenv
'''
uvicorn main:app --reload
http://127.0.0.1:8000
'''
from fastapi import FastAPI


app = FastAPI()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRED_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRED_MINUTES"))
 
from auth_routes import auth_router
from order_routes import order_router

# INCLUIR ROTEADOR
app.include_router(auth_router)
app.include_router(order_router)

