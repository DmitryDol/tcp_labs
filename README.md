# tcp_labs

Лабораторные работы по предмету "Технологии сетевого программирования"

## ЛР0

[Презентация](https://docs.google.com/presentation/d/17_LZ12iUvj4OtdCWVxXDk7pI9Y-ayiKdLRb19UnVCOQ/edit?usp=sharing)

[Отчет](https://docs.google.com/document/d/1LPiKWnQ9E7KnppfHBw2JA64IY4K4KiiCK2GvF-Naf_k/edit?usp=sharing)

## Запуск backend`а:

Сборка контейнеров

```
docker compose up -d --build
```

Накатить миграции (создать БД)

```
docker compose exec -w /app fastapi_app alembic upgrade head
```

Заполнить бд тестовыми данными

```
docker compose exec fastapi_app uv run fill_database.py
```

## Swagger и MinIO

[Swagger UI](http://localhost:8080/swagger-ui.html)

[MinIO](http://localhost:9001) (admin/password)

## Endpoints

### MinIO endpoints
| Метод      | Путь              | Описание               |
| ---------- | ----------------- | ---------------------- |
| POST       | /files            | Загрузка файла в MinIO |
| GET        | /files/{filename} | Получение файла        |
| DELETE     | /files/{filename} | Удаление файла         |
