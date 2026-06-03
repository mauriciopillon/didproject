import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from routes.forward_route import router as forward_router
from routes.health_route import router as health_router

load_dotenv()

RELAYER_HOST = os.getenv("RELAYER_HOST")
RELAYER_PORT = int(os.getenv("RELAYER_PORT"))

app = FastAPI()
app.include_router(forward_router)
app.include_router(health_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=RELAYER_HOST,
        port=RELAYER_PORT,
        reload=True
    )