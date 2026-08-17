from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from fastapi import Depends

def pegar_sessao():

    try:
        Sessao = sessionmaker(bind=db)
        sessao = Sessao()
        yield sessao  

    finally:          
        sessao.close()

def verificar_token(token, sessao: Session = Depends(pegar_sessao)): # verificar se o token é válido. se sim, extrair o id do usuario.
    usuario = sessao.query(Usuario).filter(Usuario.id==1).first() 
    return usuario # qual é o usuario que é dono do token?