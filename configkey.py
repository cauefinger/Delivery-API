from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
 
load_dotenv() 
SECRET_KEY = os.getenv("SECRET_KEY") 
bcrypt_context = CryptContext(schemes=["bcrypt"])
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form") # estar logado para implementar token na documentação fastapi