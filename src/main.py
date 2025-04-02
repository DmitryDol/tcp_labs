import uvicorn
from fastapi import FastAPI

from src.api.main import api_router
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))



<<<<<<< HEAD
async def main():
    await AsyncORM.create_tables()
=======
app = FastAPI(
    title="Сервис для трекинга карьеры"
)

app.include_router(api_router)
>>>>>>> 6071a92abb44c8e658552940319d4c3aff800f45

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)