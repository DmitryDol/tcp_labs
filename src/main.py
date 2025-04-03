import uvicorn
from fastapi import FastAPI

from api.main import api_router
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))


app = FastAPI(
    title="Сервис для трекинга карьеры"
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)