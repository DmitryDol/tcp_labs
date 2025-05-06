from contextlib import asynccontextmanager
import logging
import time
from typing import Callable
import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.main import api_router
import os
import sys

from config import configure_logging, settings

sys.path.insert(1, os.path.join(sys.path[0], '..'))

configure_logging(level=logging.DEBUG)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug('Initializing Redis client.')
    redis_client = redis.Redis(
        host=settings.REDIS_HOST, 
        port=settings.REDIS_PORT, 
        db=settings.REDIS_DB, 
        decode_responses=True
    )
    try:
        await redis_client.ping()
        logger.debug("Redis connection successful.")
        app.state.redis_client = redis_client
        yield
    finally:
        logger.debug("Closing Redis connection.")
        await app.state.redis_client.close()
        logger.debug("Redis connection closed.")

    # email_devops() to notify that server is down

app = FastAPI(
    title="Сервис для трекинга карьеры",
    lifespan=lifespan
)

origins = [
    "http://localhost:5050",
    "http://127.0.0.1:5050"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware('http')
async def add_process_time_header(request: Request, call_next: Callable):
    start_time = time.monotonic()
    response = await call_next(request)
    process_time = time.monotonic() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request {request.method} {request.url.path} processed in {process_time:.4f} seconds") 
    return response


    

app.include_router(api_router)

# if __name__ == "__main__":
#     uvicorn.run(app="main:app", reload=True)