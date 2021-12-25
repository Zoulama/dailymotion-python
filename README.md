# Dailymotion python service

The Dailymotion user service is a python 3 project that handles user Registration in a Mongo DB 

## Install python3
```
brew install python3
```
## Install pip
```
sudo easy_install pip
```
## Create and activate dailymotion-python virtual environment
```
make setup
```
## Run dailymotion-python locally
```
make up
```

## go mailtrip.io create an account and setup  values on docker-compose.yml

|                Name | Description     |
|-------------------- |-----------------|
| MAIL_SERVER         | smtp.mailtrap.io|
| MAIL_PORT           | 587             |
| MAIL_USERNAME       | username        |
| MAIL_PASSWORD       | password        |


[Head to]( http://localhost:8087)

## Update requirements.txt
```
pip freeze > requirements.txt
```

## Environment variables on docker-compose.yml

|                Name | Description   |
|-------------------- |---------------|
| DB_MONGO_USERNAME   | Username      |
| DB_MONGO_PASSWORD   | Password      |
| DB_MONGO_HOST       | Hostname      |
| DB_MONGO_PORT       | Port          |
| DB_MONGO_URI_SCHEME | Scheme        |
| DB_MONGO_DATABASE   | Database name |


## Environments
| ENVIRONMENTS | URL                                                        |
|--------------|------------------------------------------------------------|
| DEV          | http://localhost:8087      |

