FROM python:3.11-slim

RUN pip install cryptography

WORKDIR /app
COPY client.py .
COPY crypto.py .

CMD ["python", "client.py"]
