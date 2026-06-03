import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from routes.tx_route import router as tx_router
from routes.health_route import router as health_router

load_dotenv()

XRPL_COSMOS_API_HOST = os.getenv("XRPL_COSMOS_API_HOST")
XRPL_COSMOS_API_PORT = int(os.getenv("XRPL_COSMOS_API_PORT"))

app = FastAPI()
app.include_router(tx_router)
app.include_router(health_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=XRPL_COSMOS_API_HOST,
        port=XRPL_COSMOS_API_PORT,
        reload=True
    )