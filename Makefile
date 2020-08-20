.PHONY: up up_build test clean

up:
	docker-compose up -d

up_build:
	docker-compose up -d --build --force-recreate

tests:
	python3 -W ignore:ResourceWarning -m unittest discover -v -b

clean:
	docker-compose down
