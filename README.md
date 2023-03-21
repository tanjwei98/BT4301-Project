# BT4301 Project Group 2

## For first time set up (create virtual environment called .venv, and install dependencies in requirements.txt)
```
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt 
```

## To run server
```
. .venv/bin/activate
python Project/manage.py runserver
```

## To set up Postgres database 
1. Connect to your Postgres server (running on localhost) by filling in your details in `settings.py`
```
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '[EDIT],
        'USER': [EDIT],
        'PASSWORD': [EDIT],
        'HOST': 'localhost',
        'PORT': [EDIT],
    }
}
```

2. Make migrations to create database schema
```
python3 Project/manage.py makemigrations core 
python3 Project/manage.py migrate core
```

## FYI - steps to take if any changes are made to the schema
1. drop all relevant migration files in `migrations` folder (e.g. `0001_initial.py`). Excluding `__init__.py` file.
2. drop cascade all relevant tables via PGAdmin4 (table anmes start with "core_")
3. make migrations by running `python3 Project/manage.py makemigrations core`
4. run `python3 Project/manage.py migrate --fake core zero`
5. migrate by running `python3 Project/manage.py migrate core`