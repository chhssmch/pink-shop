# Берем базовый образ с Python
FROM python:3.12-slim
# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app


# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Копируем весь остальной код проекта
COPY . .
# Собираем статику (для админки и DRF)
RUN python manage.py collectstatic --noinput
# Команда для запуска приложения (используем daphne, так как у нас веб-сокеты)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "my_project.asgi:application"]
