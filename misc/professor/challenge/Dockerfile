FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./ /app

RUN mkdir -p /app/uploads

RUN pip install --no-cache-dir -r requirements.txt

ENV GEMINI_API_KEY=

COPY gcloud_key.json /app/gcloud_key.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/gcloud_key.json

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
