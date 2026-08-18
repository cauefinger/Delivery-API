from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from fastapi import Depends, HTTPException  
from main import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from configkey import oauth2_schema
def pegar_sessao():

    try:
        Sessao = sessionmaker(bind=db)
        sessao = Sessao()
        yield sessao  

    finally:          
        sessao.close()


def verificar_token(token:str = Depends(oauth2_schema), sessao: Session = Depends(pegar_sessao)):

    try:
        dic_info = jwt.decode(token,SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        HTTPException(status_code=401, detail="Acesso negado, verifique a validade do token.")


    usuario = Session.query(Usuario). filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso inválido.")
    return usuario

