from datetime import datetime
from typing import Callable
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from api.main import api_router
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))


app = FastAPI(
    title="Сервис для трекинга карьеры"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production заменить на список конкретных доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)