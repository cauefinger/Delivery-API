from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema 
from models import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])  


@order_router.get("/")
async def pedidos():
    return {"mensagem": "Você acesssou a rota de pedidos"}


@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, sessao: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    sessao.add(novo_pedido)
    sessao.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}