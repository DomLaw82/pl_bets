rm -f db_dump.sql
pg_dump pl_stats -F p -h localhost -p 5432 -U postgres > db_dump.sql