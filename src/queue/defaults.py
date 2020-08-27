#!/usr/bin/env python3

from os import environ


class DefaultValues:
    RABBITMQ_HOST = str(environ.get("RABBITMQ_HOST", default="localhost"))
    RABBITMQ_PORT = int(environ.get("RABBITMQ_PORT", default=5672))

    TASK_QUEUE = "task_queue"
    RESPONSE_QUEUE = "response_queue"
