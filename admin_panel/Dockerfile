FROM python:3.10.0-slim-buster

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update -qq \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
        build-essential \
        git \
        vim \
        curl \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && truncate -s 0 /var/log/*log

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
ENV PATH="${PATH}:/root/.local/bin"
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install  --no-interaction --no-ansi

ENV DJANGO_SETTINGS_MODULE="todo.settings"

COPY . /app

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8001
#CMD uwsgi --http :8000 --module todo.wsgi --enable-threads