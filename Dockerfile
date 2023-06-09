FROM python:3.10

WORKDIR /app

# Install poetry:
RUN pip install poetry

# Copy in the config files:
COPY pyproject.toml poetry.lock ./
# Install only dependencies:
RUN poetry install --no-root --no-dev

# Copy in everything else and install:
COPY ./src ./src
RUN poetry install --no-dev

ENTRYPOINT ["poetry", "run", "python", "/app/src/main.py"]