.SILENT:

include .env

PSQL_IMAGE_NAME = pl_postgres
PSQL_CONTAINER_NAME = pl_bets
DATABASE = $(local_db_name)
USERNAME = $(local_db_username)
PASSWORD = $(local_db_password)

.PHONY: build_postgres run_postgres enter_shell start_postgres rebuild_postgres

build_postgres:
	docker build -t $(PSQL_IMAGE_NAME) .

run_postgres:
	docker run -d --name $(PSQL_CONTAINER_NAME) -p 5432:5432 $(PSQL_IMAGE_NAME)

stop_postgres:
	docker stop $(PSQL_CONTAINER_NAME)

remove_postgres:
	docker rm -f $(PSQL_CONTAINER_NAME)

enter_shell:
	PGPASSWORD=$(PASSWORD) psql -h localhost -p 5432 -U $(USERNAME) -d $(DATABASE)

sleep:
	sleep 2

start_postgres: 
	docker start $(PSQL_CONTAINER_NAME)

rebuild_postgres: remove_postgres build_postgres run_postgres sleep enter_shell

restart_postgres: stop_postgres start_postgres sleep enter_shell
