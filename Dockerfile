FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir . fastapi uvicorn python-multipart httpx

EXPOSE 8000
CMD ["uvicorn", "crochet_checker.web.app:app", "--host", "0.0.0.0", "--port", "8000"]
