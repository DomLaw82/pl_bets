# Use the official PostgreSQL image from Docker Hub
FROM postgres:16.1

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y python3 python3-pip

RUN apt install -y python3-pandas && \
    apt install -y python3-psycopg2 && \
    apt install -y python3-sqlalchemy && \
    apt install -y python3-bs4

CMD ["python3", "app/ingestion/__init__.py"]