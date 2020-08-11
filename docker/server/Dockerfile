FROM python:3.8-alpine as osint-framework-server

LABEL org.label-schema.name="OSINT Framework Server" \
      org.label-schema.description="OSINT Framework Server" \
      org.label-schema.license="GPL-2.0"

COPY . /app/
COPY docker/server/wait-for-it.sh /app/wait-for-it.sh
WORKDIR /app
RUN apk add --no-cache --virtual .build_deps build-base libffi-dev gcc musl-dev && \
    apk add --no-cache postgresql-dev bash && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build_deps && \
    chmod +x wait-for-it.sh

EXPOSE 8888
ENTRYPOINT ["./wait-for-it.sh", "-t", "5", "osint-framework-db:5432", "--", "python3", "server.py"]
