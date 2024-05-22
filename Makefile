.PHONY: run-etl restart-etl

run-etl:
	docker-compose up -d etl

restart-etl:
	docker-compose stop etl
	docker-compose up -d etl
