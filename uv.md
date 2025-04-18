Установка UV на windows
```
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Или через pip
```
pip install uv
```

Создание окружения
```
uv venv
```

Активация окружения
```
.venv\Scripts\activate
```

Если не работает, то Ctrl+Shift+P, далее ввести в поиске Python: Select Interpreter и выбрать интерпретатор из этого виртуального окружения

Установка библиотек
```
uv pip install fastapi # Ставим fastapi

uv pip install -r requirements.txt # Установка из requirements.txt
```

Обновить requirements.txt
```
uv pip freeze | uv pip compile - -o requirements.txt
```