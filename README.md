# Django-Doker-Restful-E_Commerce
# Hamid Mottaghian FullStack Developer,



Create Ecommerce with Python and djanro framework, Docker and Rest Framework



Used pinenv and ubuntu 16.0 and Docker


1- $ sudo pip3 install pipenv
2- $ pipenv shell

Create Dockerfile

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




Create requirements.txt
{
Django>=3.0.4,<3.1.0
djangorestframework>=3.11.0,<3.10.0
}


Create a new folder and rename it, app

NOTE: We are used alpine image and this progress must be fast
Build Dockerfile
1- $ docker build .


We can create a docker-compose configuration for our project
NOTE:   Docker-compose is a tool that allows to run a docker image easlly from project location.
        Docker Compose is used to run multiple containers as a single service. For example, suppose you had an application which required NGNIX and MySQL, you could create one file which would start both the containers as a service without the need to start each one separately.



Create docker-compose.yml

________________________________________________________________________________________
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
___________________________________________________________________________________________



Create Django project with Docker Configurations
We used docker-compose to run a command on our image that contains the django dependents it and we will create a project for our application.

$ docker-compose run app sh -c "django-admin startproject app ."



NOTE: What is Travis: Travis is really useful tool for my project that we can used for auto test and check our project when push on github, every times.
Go to https://travis-ci.org/ and signin with github



Create a travis file : .travis.yml
firt we have to tell, what language did we use that is python
_____________________________________________________________________________________________
    language: python
    python:
        - "3.6"

    services:
        - docker

    before_script: pip install docker-compose

    script:
        - docker-compose run app sh -c "python manage.py test && flake8"
__________________________________________________________________________________________







NOTE: We are using flake8, this a modular code checker and we have to install it.
      Go to python package index (pypi) https://pypi.org and added last version in to requirenment.txt

Create .flake8 file in app folder (manage.py location) and type :

_____________________________________________________________________________________
    [flake8]
    exclude = 
        migrations
        __pycache__,
        manage.py,
        settings.py
____________________________________________________________________________________




Example Unit Test(Test-driven development (TDD))
Create calc.py in app/app (settings.py location) and write :

______________________________________________________________________________
    def add(x,y):
        """ADD TOW NUMBER TOGETHER"""
        return x+y

    def subtract(x,y):
        """Substract x from y and return value"""
        return y-x
______________________________________________________________________________




Create tests.py in app/app (settings.py location) and write :

from django.test import TestCase
from app.calc import add,subtract
____________________________________________________________________________

class CalcTests(TestCase):

    def test_add_numbers(self):
        """Test that two number are added together"""
        self.assertEqual(add(3,8),11)
    
    def test_subtract_numbers(slef):
        """Test that values are substracted and returned"""
        self.assertEqual(subtract(5,11),6)
______________________________________________________________________________

Eexample Run test:
$ docker-compose run app sh -c "python manage.py test && flake8"


Create New APP in ourproject with docker-compose:
$ docker-compose run app sh -c "python manage.py startapp core"
Our APP name is "core"

NOTE: Delete views.py in core application beacuse in core we dont needed it and Create a __init__.py  and test_models.py in tests folder.

in tets_models.py :
________________________________________________________________________________
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test Creating a new user with an email"""
        email = 'hammott@hammott.ir'
        password = 'test1234'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalizer"""
        email = 'hammott@hammott.ir'
        user = get_user_model().objects.create_user(email, 'test1234')

        self.assertEqual(user.email, email.lower())
_____________________________________________________________________________
And for run test unit
$ docker-compose run app sh -c "python manage.py test"





Create Custom User Model in core app:
________________________________________________________________________________
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                                        BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and Saves a new user"""
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user



class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that support using email instead of username"""
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()
    USERNAME_FIELD = 'email'

___________________________________________________________________________________________
User model must define in settings.py : 
AUTH_USER_MODEL = 'core.User' ('name of the app. name of the user class in models.py')


Make Migrations with docker-compose
$ docker-compose run app sh -c "python manage.py makemigrations core"






Add Validation for email field:

test_models.py in ModelTest class:
__________________________________________________________________________________________
def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')
__________________________________________________________________________________________

UserManager class in models.py:
_________________________________________________________________________________________
if not email:
            raise ValueError('Users must have and email address')
__________________________________________________________________________________________

and test unit items:
$ ocker-compose run app sh -c "python manage.py test"





Create Super User:
test_models.py in ModelTest class:
______________________________________________________________________________________
    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'hammott@hammott.ir',
            'test1234'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
_____________________________________________________________________________________

UserManager class in models.py:
_____________________________________________________________________________________
    def create_superuser(self,email,password):
        """Create and Sacves a super user"""
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using= self._db)

        return user
_______________________________________________________________________________________




and test unit items:
$ ocker-compose run app sh -c "python manage.py test"





Create admin for my application
___________________________________________________________________________________
in test_admin.py:

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@hammott.ir',
            password = 'password1234'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'hammott@hammott.ir',
            password = 'password1234',
            name = 'Test user full name'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page work"""
        url = reverse ('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that create user page works"""
        url = reverse ( 'admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
________________________________________________________________________________________

________________________________________________________________________________________
admin.py:

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext
from core import models

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields':('email','password')}),
        (gettext('Personal Info'),{'fields': ('name',)}),
        (
            gettext('Permissions'),
            {
                'fields':(
                    'is_active',
                    'is_staff' 
                    'is_superuser'
                )
            }
        ),
        (gettext('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

admin.site.register(models.User, UserAdmin)

________________________________________________________________________________________


again Run Unit Test:
$ docker-compose run app sh -c "python manage.py test && flake8"

