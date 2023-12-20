# Use the official PostgreSQL image from Docker Hub
FROM postgres:16.1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3 python3-pip

RUN apt install -y python3-pandas && \
    apt install -y python3-psycopg2 && \
    apt install -y python3-sqlalchemy && \
    apt install -y python3-bs4 && \
    apt install -y python3-fuzzywuzzy

COPY . .

CMD ["python3", "__init__.py"]