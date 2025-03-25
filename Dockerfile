FROM python:3.13-slim

WORKDIR /salary-project
RUN pip install poetry \
    && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main

COPY . .
RUN chmod +x ./entrypoint.sh

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]