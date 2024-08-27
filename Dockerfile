# Используем официальный образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем файлы зависимостей и устанавливаем их
COPY ./TB4/requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем оставшиеся файлы проекта
COPY ./TB4/ /code/

# Устанавливаем переменную окружения
ENV PYTHONUNBUFFERED 1

# Команда для запуска приложения
# Команда для выполнения миграций и запуска приложения
CMD ["sh", "-c", "python TB4/manage.py migrate && python TB4/manage.py runserver 0.0.0.0:8000"]

