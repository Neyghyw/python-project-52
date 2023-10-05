### Hexlet tests and linter status:
[![Actions Status](https://github.com/Neyghyw/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/Neyghyw/python-project-52/actions)

### CodeClimate (Maintainability and linter)
[![Maintainability](https://api.codeclimate.com/v1/badges/8afa2c425bd854052cf1/maintainability)](https://codeclimate.com/github/Neyghyw/python-project-52/maintainability)

### Description
Hello!

This web app is simple task manager on Django.
Here you can create your tasks. Task has status and labels(optional).
This project has english-russian localization.


The app is available by link: https://task-manager-dhm9.onrender.com

### Local usage
For personal usage you need to do some commands:
```
poetry install
python manage.py migrate
python manage.py ruserver
```

### Tech stack
* Linux OS
* python = "^3.7"
* dj-database-url = "^2.0.0"
* django-bootstrap5 = "^23.3"
* django-filter = "^23.3"
* gunicorn = "^21.2.0"
* whitenoise = "^6.5.0"
* psycopg2-binary = "^2.9.8"
* rollbar = "^0.16.3"
