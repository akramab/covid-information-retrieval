FROM python:3.9-slim

COPY ./app /app/src
COPY ./test /app/test
COPY ./requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "15400"]

