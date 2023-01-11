
docker-build:
	docker-compose -f init.yml build --force-rm initdb

local-create:
	docker-compose -f init.yml -f airflow.yml up -d --build

local-remove:
	docker-compose -f init.yml -f airflow.yml down --volumes

local-recreate: local-remove local-create

