FROM python:3.8-alpine as osint-framework-consumer

LABEL org.label-schema.name="OSINT Framework Consumer" \
      org.label-schema.description="OSINT Framework Consumer" \
      org.label-schema.license="GPL-2.0"

COPY . /app/
COPY docker/server/wait-for-it.sh /app/wait-for-it.sh
COPY docker/consumer/consumer.py /app/consumer.py
WORKDIR /app
RUN apk add --no-cache --virtual .build_deps build-base libffi-dev gcc musl-dev && \
    apk add --no-cache postgresql-dev bash curl && \
    # If you don't want to use selenium-based/chromedriver-based modules - comment the following line:
    apk add --no-cache unzip libexif udev chromium chromium-chromedriver xvfb && \
    pip install --no-cache-dir -r requirements.txt && \
    # If you don't want to use selenium-based/chromedriver-based modules - comment the following line:
    pip install --no-cache-dir pyvirtualdisplay && \
    apk del .build_deps && \
    chmod +x wait-for-it.sh

# If you don't want to use selenium-based/chromedriver-based modules - comment the following line:
ENV DISPLAY=:99

ENTRYPOINT ["./wait-for-it.sh", "-t", "5", "osint-framework-rabbitmq:5672", "--", "python3", "consumer.py"]
