FROM python:3.7-alpine
COPY . /app
WORKDIR /app
# Necessary for psycopg2
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install pipenv
RUN pipenv install

CMD pipenv run flask run --host=0.0.0.0