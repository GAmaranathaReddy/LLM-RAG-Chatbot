FROM python:3.12-slim

WORKDIR /app

COPY ./  /app

COPY ./pyproject.toml /code/pyproject.toml
COPY ./README.md /code/README.md
RUN pip install /code/.

CMD ["sh", "hospital_neo4j_etl/entrypoint.sh"]