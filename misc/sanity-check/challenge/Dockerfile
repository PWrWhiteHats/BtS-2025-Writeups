FROM python:3.12.10-alpine3.20
ENV GEMINI_API_KEY=

RUN python3 -m pip install poetry gunicorn

WORKDIR /app
COPY app/pyproject.toml app/poetry.lock /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-root

COPY app/app /app
EXPOSE 80
# run flask app with gunicorn
CMD python3 -m gunicorn -b 0.0.0.0:80 app:app
