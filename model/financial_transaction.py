from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from typing import Union

from  model import Base


class Transaction(Base):
    __tablename__ = 'financialControl'
        

    id = Column("pk_date", Integer, primary_key=True)
    title = Column(String(140))
    amount = Column(Float)
    category = Column(String(140))
    type = Column(String(140))
    createdAt = Column(DateTime, default=datetime.now())

    def __init__(self, title:str, amount:float, category:str, type:str,
                 createdAt:Union[DateTime, None] = None):
        """
        Cria uma transação financeira

        Arguments:
            title: descrição da transação.
            amount: valor da transação
            category: categoria da transação financeira
            type: tipo da transação, entrada ou saida
            createdAt: data de quando a transação foi efetivada
        """
        self.title = title
        self.amount = amount
        self.category = category
        self.type = type

        # se não for informada, será o data exata da inserção no banco
        if createdAt:
            self.createdAt = createdAt
