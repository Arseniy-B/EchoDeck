FROM python:3.13-slim

COPY requirements.txt requirements.txt
RUN apt-get update
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --reload --port 8000 --host 0.0.0.0"]
