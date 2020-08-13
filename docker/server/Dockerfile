FROM python:3.8-alpine as osint-framework-server

COPY . /app/
COPY docker/server/wait-for-it.sh /app/wait-for-it.sh
WORKDIR /app

RUN apk add --no-cache postgresql-dev bash curl && \
    apk add --no-cache --virtual .build_deps build-base libffi-dev gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build_deps && \
    chmod +x wait-for-it.sh

EXPOSE 8888
ENTRYPOINT ["./wait-for-it.sh", "-t", "5", "osint-framework-db:5432", "--", "python3", "server.py"]
