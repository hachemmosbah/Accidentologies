FROM python:3.11

WORKDIR /Accidentologies/

COPY requirements.txt requirements.txt

RUN /bin/sh -c pip install -r requirements.txt

COPY . . 

CMD python manage.py --runserver
