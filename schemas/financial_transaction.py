from pydantic import BaseModel
from typing import List
from model.financial_transaction import Transaction
from datetime import datetime




class TransactionSchema(BaseModel):
    """ Define como uma nova transação deve ser apresentada
    """
    title: str = "Aluguel"
    amount: int = 3500
    category: str = "casa"
    type: str = 'withdraw'
    createdAt = datetime
       
    
class TransactionSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na data de inserção da transação.
    """
    transaction_id: int = 1


class TransactionListSchema(BaseModel):
    """ Define como uma listagem de transações será retornada.
    """
    transactions:List[TransactionSchema]


def transactions_show(transactions: List[Transaction]):
    """ Retorna uma representação da transação seguindo o schema definido em
        TransactionViewSchema.
    """
    result = []
    for transaction in transactions:
        result.append({
            "id": transaction.id,
            "title": transaction.title,
            "amount": transaction.amount,
            "category": transaction.category,
            "type": transaction.type,
            "createdAt": transaction.createdAt,
        })

    return {"transactions": result}


class TransactionViewSchema(BaseModel):
    """ Define como uma transação será retornada
    """
    id: int = 1
    title: str = "Aluguel"
    amount: float = 5000
    category: str = "casa"
    Type: str = 'deposit'
    createdAt: datetime = datetime.today().day


class TransactionDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    title: str

def transaction_show(transaction: Transaction):
    """ Retorna uma representação da transação seguindo o schema definido em
        TransactionViewSchema.
    """
    return {
        "id": transaction.id,
        "title": transaction.title,
        "amount": transaction.amount,
        "category": transaction.category,
        "type": transaction.type,
        "createdAt": transaction.createdAt,
    }
