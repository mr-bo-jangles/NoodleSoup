FROM python:3.12

WORKDIR /app

# Install poetry:
RUN pip install poetry

# Make the sources roots
RUN mkdir -p /app/src

# Copy in the config files:
COPY pyproject.toml poetry.lock /app/

# Install only dependencies:
RUN poetry install --no-root --no-dev

# Copy in everything else and install:
COPY ./src /app/src

RUN mkdir -p /app/src/db/

RUN poetry install --no-dev

ENTRYPOINT ["poetry", "run", "python", "/app/src/main.py"]