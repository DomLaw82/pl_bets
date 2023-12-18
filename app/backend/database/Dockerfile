# Use the official PostgreSQL image from Docker Hub
FROM postgres:16.1

RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV POSTGRES_DB=pl_bets
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password

# Initialize correct tables and database
COPY db_setup/init.sql /docker-entrypoint-initdb.d/

# Expose the default PostgreSQL port
EXPOSE 5432

# Start PostgreSQL server
CMD ["postgres"]

CMD ["python3", "./ingestion/__init__.py"]