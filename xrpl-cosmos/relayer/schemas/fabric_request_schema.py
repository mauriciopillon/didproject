from pydantic import BaseModel


class FabricRequest(BaseModel):
    amount: str
    sender: str
    receiver: str