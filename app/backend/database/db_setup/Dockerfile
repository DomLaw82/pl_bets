# Use the official PostgreSQL image from Docker Hub
FROM postgres:16.1

WORKDIR /app

ENV POSTGRES_DB=pl_stats
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password

COPY ./init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432

CMD ["postgres"]