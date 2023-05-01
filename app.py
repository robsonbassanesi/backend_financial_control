from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect


from model import Session, Transaction
from schemas import *
from schemas.financial_transaction import transaction_show

info = Info(title="Financial Control API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
transaction_tag = Tag(name="Transação", description="Adição, visualização e remoção de transações à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/transaction', tags=[transaction_tag],
          responses={"200": TransactionViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_transactions(form: TransactionSchema):
    """Adiciona uma nova transação a base de dados

    Retorna uma representação das transações.
    """
    transaction = Transaction(
        title=form.title,
        amount=form.amount,
        category=form.category,
        type=form.type,
        # createdAt=form.createdAt
        )

    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(transaction)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return transaction_show(transaction), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Erro de integridade, verifique os valores inseridos"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar nova transação :/"
        return {"mesage": error_msg}, 400
    
@app.get('/transactions', tags=[transaction_tag],
         responses={"200": TransactionListSchema, "404": ErrorSchema})
def get_transactions():
    """Faz a busca por todas as transações cadastradas

    Retorna uma representação da listagem de transações.
    """  
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    transactions = session.query(Transaction).all()

    if not transactions:
        # se não há transações cadastradas
        return {"transactions": []}, 200
    else:
        # retorna a representação da transação
        print(transactions)
        return transactions_show(transactions), 200


@app.get('/transaction', tags=[transaction_tag],
         responses={"200": TransactionViewSchema, "404": ErrorSchema})
def get_transaction(query: TransactionSearchSchema):
    """Faz a busca por uma transação a partir de seu ID

    Retorna uma representação das transações.
    """
    transaction_id = query.transaction_id
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    transaction = session.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not transaction:
        # se o produto não foi encontrado
        error_msg = "Transação não encontrada na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de produto
        return transaction_show(transaction), 200


@app.delete('/transaction', tags=[transaction_tag],
            responses={"200": TransactionDelSchema, "404": ErrorSchema})
def del_transaction(query: TransactionSearchSchema):
    """Deleta uma transação a partir de um ID informado

    Retorna uma mensagem de confirmação da remoção.
    """
    transaction_id = query.transaction_id

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Transaction).filter(Transaction.id == transaction_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Transação removido", "id": transaction_id}
    else:
        # se o produto não foi encontrado
        error_msg = "Transação não encontrada na base :/"
        return {"mesage": error_msg}, 404
