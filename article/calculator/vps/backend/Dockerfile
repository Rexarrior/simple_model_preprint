FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DB_PATH=/data/shared-calculations.sqlite3

WORKDIR /app
COPY server.py ./server.py

RUN addgroup -S app && adduser -S -G app app \
    && mkdir -p /data \
    && chown app:app /data

USER app
EXPOSE 8000

CMD ["python", "server.py"]
