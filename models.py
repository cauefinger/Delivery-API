'''
nesse arquivo vamos criar as classes de banco dados utilizando:
SQLITE e SQLALCHEMY e importando com ALEMBIC
'''

from sqlalchemy import create_engine, Column, String, Boolean, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from enum import Enum
from sqlalchemy import Enum as SQLEnum


# cria a conexão do seu banco de dados local
db = create_engine("sqlite:///banco.db")

# cria a base do banco de dados local
Base = declarative_base()   

# Utilar a base do Sqlite e colocar parâmetros 
# Transformar os parâmetros por colunas utilizando (Column, de sqlalchemy.orm)

# primary_key=True - não deve existir mais de um usuario com o mesmo id
# autoincrement=True - distrubuir o id em ordem 

# criando classe/tabela do db
class Usuario(Base):
    __tablename__ = "usuarios"
    # tabela
    id = Column("id",Integer, primary_key=True, autoincrement=True) 
    nome = Column("nome",String)
    email = Column("email",String,nullable=False) #nulo = falso         
    senha = Column("senha",String)
    ativo = Column("ativo",Boolean)
    admin = Column("admin",Boolean, default=False)

    # classe
    def __init__(self, nome, email, senha, ativo=True, admin=False):

        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
    # passar todos os parâmetros para o def init

class Status_Pedido(str, Enum):

    PENDENTE = "PENDENTE"
    CANCELADO = "CANCELADO"
    FINALIZADO = "FINALIZADO"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column("id",Integer, primary_key=True, autoincrement=True) 
    status = Column(
        SQLEnum(Status_Pedido),
        nullable=False,
        default=Status_Pedido.PENDENTE
        )
    usuario = Column("usuario", ForeignKey("usuarios.id")) # ForeignKey - quer dizer que o item pertence a outra tabela. nesse caso, é o id
    preco = Column("preço", Float)
#    itens = 

    def __init__(self, usuario, preco=0, status="PENDENTE"):

        self.usuario = usuario
        self.preco = preco
        self.status = status


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id",Integer, primary_key=True, autoincrement=True) 
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido",ForeignKey("pedidos.id"))
    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):

        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
    