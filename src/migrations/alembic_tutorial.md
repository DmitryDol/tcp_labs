# Alembic

Инициализация alembic в папку src/migrations

```
alembic init src/migrations 
```

Создание первой миграции. Флаг --autogenerate отвечает за сравнение состояния моделей в коде с состоянием в БД.

```
alembic revision --autogenerate
```

Накатить все миграции на бд. aa3097eeb005 номер последней миграции, которую нужно накатывать

```
alembic upgrade head 0b0476ca9dfb
```

Последующее создание миграций. "migration2" - название

```
alembic revision --autogenerate -m "migration2"
```

Откат на ревизию с номером `aa3097eeb005`

```
alembic downgrade aa3097eeb005
```

Откатить все миграции

```
alembic downgrade base
```
