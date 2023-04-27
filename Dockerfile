FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

RUN curl -sSL https://install.python-poetry.org | python3 -

#RUN apk update && apk add --no-cache \
#    # Required for installing/upgrading postgres, Pillow, etc:
#    gcc python3-dev \
#    # Required for installing/upgrading postgres:
#    postgresql-libs postgresql-dev musl-dev

RUN pip install psycopg2-binary
# Set work directory
RUN mkdir /code
WORKDIR /code

# Install dependencies into a virtualenv
#RUN poetry install
#
## Copy project code
COPY . /code/

RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi"]