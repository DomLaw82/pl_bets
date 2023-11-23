# Use the official PostgreSQL image from Docker Hub
FROM postgres:16.1

# Set environment variables
ENV POSTGRES_DB=pl_bets
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password

# Initialize correct tables and database
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the default PostgreSQL port
EXPOSE 5432

# Start PostgreSQL server
CMD ["postgres"]