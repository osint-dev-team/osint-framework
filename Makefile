.PHONY: clean up up_build

up:
	docker-compose up -d

up_build:
	docker-compose up -d --build --force-recreate

clean:
	docker-compose down