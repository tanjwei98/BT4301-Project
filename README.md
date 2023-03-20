# BT4301-Project

## Packages to install [will remove this section later]
- django
- psycopg2-binary==2.9.3 (for postgresql)
- djangorestframework
- pandas
- pscript (Python to Javascript)
- Js2Py (Javascript to Python)




## FIRST TIME SET UP (create virtual environment called .venv, and install dependencies in requirements.txt)
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


## To make migrations for database
```
python3 Project/manage.py makemigrations core 
python3 Project/manage.py migrate core
```