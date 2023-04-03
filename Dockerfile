FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

ENV DB_PORT=5432
ENV POSTGRES_HOST=db

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD python Project/manage.py runserver 0.0.0.0:8000