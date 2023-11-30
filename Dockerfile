FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY src/backend ./

COPY entrypoint_server.sh entrypoint_worker.sh .env requirements.txt ./

RUN pip3 install -r ./requirements.txt --no-cache-dir

RUN chmod +x entrypoint_server.sh
RUN chmod +x entrypoint_worker.sh