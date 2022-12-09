FROM python:3.10.8-slim

RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /opt/app
COPY . .
RUN pip install -r requirements.txt
WORKDIR /opt/app/mainapp
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]