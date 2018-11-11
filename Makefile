DOCKER_COMPOSE_DEV=docker-compose-dev.yml
MANAGE=python manage.py

runserver: 
	$(MANAGE) runserver

shell:
	$(MANAGE) shell_plus

start-dbs:
	docker-compose -f $(DOCKER_COMPOSE_DEV) up -d postgresql

stop-dbs:
	docker-compose -f $(DOCKER_COMPOSE_DEV) down
