from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from configkey import bcrypt_context
from schemas import UsuarioSchemas
from schemas import LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from main import ACESS_TOKEN_EXPIRED_MINUTES, ALGORITHM, SECRET_KEY   


auth_router = APIRouter(prefix="/auth", tags=["autentificação"])
'''  todo inicio de rota tem o "auth" porque esse é o nosso prefixo
essa é a rota padrão de autentificação do nosso sistema. 
'''


def autenticar_usuario(email, senha, sessao):
    usuario = sessao.query(Usuario).filter(Usuario.email==email).first() 
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario


@auth_router.get("/")
async def autenticar():
    return {"mensagem": "você acessou a rota padrão de autentificação", "autenticado": False}


@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchemas, sessao = Depends(pegar_sessao)):


    usuario =  sessao.query(Usuario).filter(Usuario.email==usuario_schema.email).first()

    if usuario:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado.")
    
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha) # criptografar senha
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada)    
        sessao.add(novo_usuario)
        sessao.commit()
        return{"mensagem": f"Usuário cadastrado com sucesso {novo_usuario.email}"} 


def criar_token(usuario_id, duracao_token = timedelta(minutes= ACESS_TOKEN_EXPIRED_MINUTES)):

    data_expiracao = datetime.now(timezone.utc) + duracao_token # datetime + 30 min
    dic_info = {
        "sub": usuario_id, 
        "exp": data_expiracao 
        } 
    jwt_codificado = jwt.encode(dic_info,SECRET_KEY, ALGORITHM )
    return jwt_codificado

def verificar_token(token, sessao: Session = Depends(pegar_sessao)):                                                                    # se sim, extrair o id do usuario.
    usuario = sessao.query(Usuario).filter(Usuario.id==1).first() 
    return usuario 


@auth_router.post("/login") 

async def login(login_schema: LoginSchema, sessao: Session  = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, sessao)

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas.")
    
    else:
        acess_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))

        return{
            "acess_token": acess_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
               }

@auth_router.get("/refresh")

async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    acess_token = criar_token(usuario.id)
    return{
            "acess_token": acess_token,
            "token_type": "bearer"
               }