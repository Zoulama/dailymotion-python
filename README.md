# Dailymotion python service

The Dailymotion user service is a python 3 project that handles user Registration in a Mongo DB 

## Clone  project
```
git clone https://github.com/Zoulama/dailymotion-python.py.git
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

## Go to mailtrip.io , create an account and setup conf values on docker-compose.yml

|                Name | Description     |
|-------------------- |-----------------|
| MAIL_SERVER         | smtp.mailtrap.io|
| MAIL_PORT           | 587             |
| MAIL_USERNAME       | username        |
| MAIL_PASSWORD       | password        |


[Head to]( http://localhost:8087)

## Environments
| ENVIRONMENTS | URL                                                        |
|--------------|------------------------------------------------------------|
| DEV          | http://localhost:8087      |


## down container
```
make down
```