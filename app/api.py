""" Controller API for communication throughout the application """

from concurrent.futures import ThreadPoolExecutor
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import health, database
from app.config.documentation import DESCRIPTION
from app.config.logging_config import create_logger


""" Logging Function """

Logger = create_logger()
Logger.info("=> Logging initialized.")


""" Multithreading Option """

executor = ThreadPoolExecutor(1)
Logger.info("=> Thread Pool established.")


""" API """

app = FastAPI(
    title="mongoDB+FastAPI",
    version="0.6.9",
    contact={
        "name": "Yannick Ciomer",
        "email": ""
    },
    summary="mongoDB Database with a FastAPI for handling read and write operations.",
    description=DESCRIPTION
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

app.include_router(health.router)
app.include_router(database.router)


""" Testing """

if __name__ == "__main__":
    # Terminal: uvicorn app.api:app --reload --host 0.0.0.0 --port 8001
    Logger.info("=> Running mongoDB+FastAPI.")
    uvicorn.run("api:app", reload=True, port=8001)
