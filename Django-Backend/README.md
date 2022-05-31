# SmartClassRoom-Backend 

<img src="https://user-images.githubusercontent.com/32195170/166079709-4a57ce5f-a0fa-4a98-8f06-88b81d868cfe.png" width="auto" height="235">

- REST Django Backend for cde2 Smart Classroom Challenge
- REST API for wdb Mini Challenge 1

## Run Django Server
1. `cd SmartClassRoom`
2. `pip -r requirements.txt`
3. `python manage.py runserver`

## Test REST API
1. `cd SmartClassRoom`
2. `python manage.py test`


## Timescale Docker Installation
https://docs.timescale.com/install/latest/installation-docker/#set-up-the-timescaledb-extension

1. Command: 
```
docker run -d --name timescaledb -p 5432:5432 \
-v /your/data/dir:/var/lib/postgresql/data \
-e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg14
```
2. add the database settings to the settings.py in the root dir:

```python
DATABASES = {
        'default': {
            'ENGINE': 'timescale.db.backends.postgresql',
            'NAME': 'DBNAME',
            'USER': 'YOURDBUSER',
            'PASSWORD': 'YourPassword',
            'HOST': 'YOURLOCALPORT',
            'PORT': '5432',
            'TEST': {
                'NAME': 'smartclassroom_test_unittest',
            },
        }
    }
```


## Django Admin Dashboard
http://127.0.0.1:8000/admin/

- username: `admin`
- password: `Welcome12`

## Database Migration after Model Changes

1. `python manage.py makemigrations`
2. `python manage.py migrate`

Made with ❤️ and  🥥
