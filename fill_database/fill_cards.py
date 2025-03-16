import asyncio
from database import SessionLocal
from orm_models import Card

async def add_cards():
    async with SessionLocal() as session:
        cards = [
            Card(
                title="Введение в машинное обучение",
                description="Основные концепции ML: что это такое, какие бывают виды (обучение с учителем, без учителя и с подкреплением), примеры применения."
            ),
            Card(
                title="Основы линейной алгебры и статистики",
                description="Матрицы, векторы, вероятность, распределения – математический фундамент для работы с данными и построения моделей."
            ),
            Card(
                title="Работа с данными в Python",
                description="Библиотеки Pandas и NumPy, загрузка, обработка, очистка и визуализация данных перед обучением модели."
            ),
            Card(
                title="Основные модели машинного обучения",
                description="Линейная регрессия, логистическая регрессия, деревья решений – базовые алгоритмы, которые нужно знать."
            ),
            Card(
                title="Метрики качества моделей",
                description="Как оценивать эффективность моделей: MSE, RMSE, Precision, Recall, F1-score и другие метрики."
            ),
            Card(
                title="Обучение с учителем и без учителя",
                description="Различия между supervised и unsupervised learning, примеры алгоритмов для каждого подхода."
            ),
            Card(
                title="Гиперпараметры и их настройка",
                description="GridSearch, Random Search, кросс-валидация – методы для улучшения производительности моделей."
            ),
            Card(
                title="Глубокое обучение (основы)",
                description="Введение в нейросети, основные архитектуры, фреймворки TensorFlow и PyTorch."
            ),
            Card(
                title="Развертывание моделей ML",
                description="Как сохранить модель, создать API для предсказаний, интегрировать ML в веб-приложение."
            )    
        ]

        session.add_all(cards)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(add_cards())