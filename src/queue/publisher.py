#!/usr/bin/env python3

from json import dumps

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from src.core.utils.log import Logger
from src.queue.defaults import DefaultValues as Default
from src.server.structures.task import TaskItem

logger = Logger.get_logger(name=__name__)


class Publisher:
    def __init__(
        self,
        host: str = Default.RABBITMQ_HOST,
        port: int = Default.RABBITMQ_PORT,
        task_queue: str = Default.TASK_QUEUE,
        response_queue: str = Default.RESPONSE_QUEUE,
    ):
        """
        Init rabbitmq publisher
        :param host: rabbitmq host
        :param port: rabbitmq port
        :param task_queue: queue name
        :param response_queue: response queue name
        """
        self.task_queue_name = task_queue
        self.response_queue_name = response_queue

        self.connection = BlockingConnection(
            ConnectionParameters(host=host, port=port,)
        )
        self.channel = self.connection.channel()

        self.task_queue = self.channel.queue_declare(queue=self.task_queue_name)
        self.response_queue = self.channel.queue_declare(queue=self.response_queue_name, exclusive=True)

        self.channel.basic_consume(
            queue=self.response_queue_name,
            on_message_callback=self.task_response,
            auto_ack=True,
        )

    @staticmethod
    def task_response(
        channel: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        """
        Process tasks response
        :param channel: channel
        :param method: method
        :param properties: task properties
        :param body: task body
        :return: None
        """
        logger.info(msg=f"Done task {properties.correlation_id}")

    def publish_task(self, task: TaskItem, cases: list) -> None:
        """
        Publish task
        :param task: task item
        :param cases: list of cases
        :return: None
        """
        task_body = dumps(
            {
                "task": task.as_json(),
                "cases": cases
            }
        ).encode(encoding="utf-8")

        self.channel.basic_publish(
            exchange="",
            routing_key=self.task_queue_name,
            properties=BasicProperties(
                reply_to=self.response_queue_name, correlation_id=task.task_id,
            ),
            body=task_body,
        )

    def process_data_events(self, time_limit: int = 1) -> None:
        """
        Process data events
        :param time_limit: limit time of processing (in seconds)
        :return: None
        """
        logger.info(
            msg=f"Check for new events: "
                f"{self.task_queue.method.message_count} tasks in queue, "
                f"{self.response_queue.method.message_count} responses in queue"
        )
        self.connection.process_data_events(time_limit=time_limit)

    def __del__(self):
        """
        Force close connection
        :return: None
        """
        try:
            self.connection.close()
        except:
            pass
