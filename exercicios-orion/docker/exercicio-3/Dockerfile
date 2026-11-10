FROM python:3.12-slim AS base

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 3000

FROM base AS dev
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]

FROM base AS prod
RUN useradd --create-home appuser
USER appuser
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
