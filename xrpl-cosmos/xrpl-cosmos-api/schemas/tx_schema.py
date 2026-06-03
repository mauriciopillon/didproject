from pydantic import BaseModel


class TransactionRequest(BaseModel):
    amount: str
    receiver: str
    sender: str