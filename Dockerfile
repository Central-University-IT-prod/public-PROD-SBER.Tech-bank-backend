# Preparing the requirements for installing
FROM python:latest as requirements-stage

WORKDIR /tmp

RUN python3 -m pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN python3 -m poetry export -f requirements.txt --output requirements.txt --without-hashes

# Installing the requirements
FROM python:latest

WORKDIR /server

COPY . /server

# Installing the dependencies
COPY --from=requirements-stage /tmp/requirements.txt /server/requirements.txt

RUN python3 -m pip install --no-cache-dir --upgrade -r /server/requirements.txt

ENV SERVER_PORT=8080

# Running the app
CMD ["sh", "-c", "uvicorn server.__main__:app --host 0.0.0.0 --port $SERVER_PORT"]