SHELL := /bin/bash

up:
	@echo "Running containers..."
	docker compose up --build

re: fclean up

down:
	@echo "Stopping containers..."
	docker compose down

logs:
	@echo "Displaying logs..."
	docker compose logs -f

fclean:
	@echo "Removing all containers and volumes..."
	docker stop $(docker ps -aq); docker rm $(docker ps -aq) -f; docker volume rm -y $(docker volume ls) -f ; docker system prune;docker volume prune -f;

volume :
	@echo "deleting all volumes..."
	docker compose down -v