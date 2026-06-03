import os
from dotenv import load_dotenv
import httpx

load_dotenv()

TRANSACTION_ROUTE = "http://" + os.getenv("XRPL_COSMOS_API_HOST") + ":" + os.getenv("XRPL_COSMOS_API_PORT") + "/" + os.getenv("TRANSACTION_ROUTE")

async def forward_post(body):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TRANSACTION_ROUTE,
            json=body.model_dump())

    return response.json()