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

## steps to run Gitlab as a docker container
+ install docker on your system
+ After installing docker, open powershell and type the command: docker pull gitlab/gitlab-ce
+ Then run the command: docker run --detach `
  --hostname gitlab.example.com `
  --publish 443:443 --publish 80:80 --publish 22:22 `
  --name gitlab `
  --restart always `
  --volume /srv/gitlab/config:/etc/gitlab `
  --volume /srv/gitlab/logs:/var/log/gitlab `
  --volume /srv/gitlab/data:/var/opt/gitlab `
  gitlab/gitlab-ce:latest
+ After this you should be able to see a running container on your docker desktop with the name gitlab and the ports given
+ Find out the name of the ipaddress of your system by typing "ipconfig" in the command line.
+ For example the ipaddress of my system is 192.168.1.109.
+ If gitlab is successfully installed as a docker container, then you would be able to access it as 192.168.1.109:80(wherein 80 is the port number mentioned in the docker gitlab container)
+ To login into gitlab you need userid and password. root is the userid. For password, tyoe in the following command in the command line: docker exec -it gitlab grep 'Password:' /etc/gitlab/initial_root_password
+ You will get a password, use it to login into gitlab

## What all new things?
+ Format of databases on settings.py is different, just enter your details
+ A new docker-compose.yml file is added to the root directory, add your database details in it.
+ A new dockerfile is added to the root directory, no details to be added to it.