FROM python:3.10-bullseye

WORKDIR /code

RUN apt update && apt install -y sqlite3
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$PATH:/root/.local/bin

COPY ./pyproject.toml ./poetry.lock /code/
RUN /root/.local/bin/poetry install

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
