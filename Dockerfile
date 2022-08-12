# syntax=docker/dockerfile:1

FROM python:3.11.0b5-alpine
WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "DyDNS.py"]
