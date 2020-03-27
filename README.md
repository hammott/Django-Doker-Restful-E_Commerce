# Django-Doker-Restful-E_Commerce
Create Ecommerce with Python and djanro framework, Docker and Rest Framework



Used pinenv and ubuntu 16.0 and Docker


1- $ sudo pip3 install pipenv
2- $ pipenv shell

Create Dockerfile
--------------------------------------------------------------------
FROM python:3.7-alpine
MAINTAINER Tehran Hamid Mottaghian


ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
----------------------------------------------------------------------



Create requirements.txt
-----------------------------------------------------------------------
Django>=3.0.4,<3.1.0
djangorestframework>=3.11.0,<3.10.0
-----------------------------------------------------------------------


Create a new folder and rename it, app

NOTE: We are used alpine image and this progress must be fast
Build Dockerfile
1- $ docker build .


We can create a docker-compose configuration for our project
NOTE:   Docker-compose is a tool that allows to run a docker image easlly from project location.
        Docker Compose is used to run multiple containers as a single service. For example, suppose you had an application which required NGNIX and MySQL, you could create one file which would start both the containers as a service without the need to start each one separately.



Create docker-compose.yml
----------------------------------------------------------------------
version: "3"

services:
    app:
        build: 
            context: .
        ports:
            - "8000:8000"
        volumes:
            - ./app:/app
        command: >
            sh -c "python manage.py runserver 0.0.0.0:8000"
----------------------------------------------------------------------


Create Django project with Docker Configurations
We used docker-compose to run a command on our image that contains the django dependents it and we will create a project for our application.

$ docker-compose run app sh -c "django-admin startproject app ."



NOTE: What is Travis: Travis is really useful tool for my project that we can used for auto test and check our project when push on github, every times.
Go to https://travis-ci.org/ and signin with github

Create a travis file : .travis.yml
firt we have to tell, what language did we use that is python
------------------------------------------------------------------
language: python
python:
    - "3.6"

services:
    - docker

before_script: pip install docker-compose

script:
    - docker-compose run app sh -c "python manage.py test && flake8"
------------------------------------------------------------------






NOTE: We are using flake8, this a modular code checker and we have to install it.
      Go to python package index (pypi) https://pypi.org and added last version in to requirenment.txt

Create .flake8 file in app folder (manage.py location) and type :
-------------------------------------------------------------------
[]