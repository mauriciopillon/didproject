from fastapi import APIRouter
from schemas.fabric_request_schema import FabricRequest
from services.forward_service import forward_post

router = APIRouter()


@router.post("/forward")
async def forward_request(body: FabricRequest):
    return await forward_post(body)