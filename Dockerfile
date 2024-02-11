FROM python:3.10

RUN mkdir /fastapi_app

WORKDIR  /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR .

CMD gunicorn -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 facebook_auth:app
