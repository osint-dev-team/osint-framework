#!/usr/bin/env python3

from json import dumps

import pika

from src.core.utils.log import Logger
from src.queue.defaults import DefaultValues as Default
from src.server.structures.task import TaskItem

logger = Logger.get_logger(name=__name__)


class Publisher:
    def __init__(self, host: str = Default.RABBITMQ_HOST, port: int = Default.RABBITMQ_PORT):
        """
        Init rabbitmq publisher
        :param host: rabbitmq host
        :param port: rabbitmq port
        """
        self.queue = Default.QUEUE
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host,
                port=port,
            )
        )
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

    def on_response(self, ch, method, props, body) -> None:
        """
        Process tasks response
        :param ch: channel
        :param method: method
        :param props: task properties
        :param body: task body
        :return: None
        """
        logger.info(msg=f"Done task {props.correlation_id}")

    def publish_task(self, task: TaskItem, cases: list) -> None:
        """
        Publish task
        :param task: task item
        :param cases: list of cases
        :return: None
        """
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=task.task_id,
            ),
            body=dumps({"task": task.as_json(), "cases": cases}),
        )

    def process_data_events(self) -> None:
        """
        Process data events
        :return: None
        """
        self.connection.process_data_events(time_limit=1)

    def __del__(self):
        """
        Force close connection
        :return: None
        """
        try:
            self.connection.close()
        except:
            pass