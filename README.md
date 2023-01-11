# Разворачивание локального Airflow для обработки api

## Краткое описание

Итоговый результат представляет собой проект, который разворачивает docker-контейнер с Airflow и Postgres(отдельной БД),
создаёт подключения и инициализирует airflow. Включен даг, который обрабатывает данные с тестового апи и обновляет
таблицу в инкрементальном режиме в БД.

## Getting Started
### Install and Running

1. Pull repository:

```shell script
git clone git@github.com:vladshatilov/airflow_api_fetch.git
```

2. Copy default environment variables from deploy.env to .env file

3. Define blank OS environment variables in deploy/.env file, for example

```.env
PROJECT_HOST_FOLDER=/path/to/project
```

4. Build docker images:

```shell script
make docker-build # build docker images
```

5. Start local environment for airflow:


```shell script
make local-create # create and run local environment
```

```shell script
make local-remove: # remove local environment and delete current state
```
