# Rest-api-django-advanced

Build a Backend REST API with Python &amp; Django - Advanced code

# Dev commands

## Export requirements for docker

`poetry export -f requirements.txt --output requirements.txt --without-hashes`

## Build docker file from this directory

`docker build .`

## Create project in compose ?

`docker-compose run --rm app sh -c "django-admin startproject app ."`
