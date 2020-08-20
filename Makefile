.PHONY: up up_build test clean

up:
	docker-compose up -d --scale consumer=5

up_log:
	docker-compose up --scale consumer=5

build:
	docker-compose up -d --build --force-recreate --scale consumer=5

build_log:
	docker-compose up --build --force-recreate --scale consumer=5

tests:
	python3 -W ignore:ResourceWarning -m unittest discover -v -b

clean:
	docker-compose down
	docker volume rm osint-framework_postgres -f
