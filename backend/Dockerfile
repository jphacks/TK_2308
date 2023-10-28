FROM python:3.10-bullseye

WORKDIR /code

RUN apt update && apt install -y sqlite3

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --requirement /code/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
