from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema 
from models import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])  


@order_router.get("/")
async def pedidos():
    return {"mensagem": "Você acesssou a rota de pedidos"}


@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, sessao: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    sessao.add(novo_pedido)
    sessao.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}


@order_router.post("/pedido/cancelar`{pedido_id}")
async def cancelar_pedido(pedido_id: int,  sessao: Session = Depends(pegar_sessao)):  
    pedido = sessao.query(Pedido).filter(pedido_id == Pedido.id).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado.")
    pedido.status = "CANCELADO"
    sessao.commit()
    return {
        "mensagem":f"Pedido de número: {pedido_id} cancelado com sucesso.",
        "pedido": pedido
    }