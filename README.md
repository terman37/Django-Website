# MyCpts

## Purpose

Web based app for personal finance management, 

- using django to practice python (replacing previous version developed with php/css/js)

- will try to include some ML techniques learned at school to predict balance/budget evolution

## Architecture

- running on AWS for testing purpose
- t2.micro instance with public ip / port 8000 open
- running on ubuntu server 18.04


## Setup / install django

```bash
sudo apt-get update -y
```

- install miniconda

  ```bash
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  sh Miniconda3-latest-Linux-x86_64.sh
  ```

- create venv named django - activate it

  ```bash
  conda create -n django python=3.7
  conda activate django
  ```

- install django

  ```bash
  pip install django
  ```

- check install

  ```bash
  django-admin --version
  ```


## Create Django project

- optional - Create folder:

  ```bash
  mkdir ~/django-project
  cd django-project
  ```

- Start project (this will create new folder structure)

  ```bash
  django-admin startproject djangoproject
  cd djangoproject
  ```

- Setup db (using sqlite)

  ```bash
  python manage.py migrate
  ```

- Create superuser

  ```
  python manage.py createsuperuser
  ```

  give username / email / password

- Allow host name

  ```bash
  nano ~/django-test/djangoproject/settings.py
  ```

  - Add at allowed hosts line,  

    ```
    ALLOWED_HOSTS = ['your_public_dns','and/or IP']
    ```

- Run development server

  ```bash
  python manage.py runserver your_public_dns:8000
  ```

- Check if it works in browser goto:

  http://your_public_dns:8000

  <img src="django_initial_setup.png" alt="django_initial_setup" style="zoom: 33%;" />

- admin page located at:

  http://your_public_dns:8000/admin

  

