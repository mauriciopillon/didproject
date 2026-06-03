from fastapi import APIRouter
from schemas.tx_schema import TransactionRequest
from services.tx_service import create_transaction

router = APIRouter()


@router.post("/transaction")
def transaction(body: TransactionRequest):
    return create_transaction(body)