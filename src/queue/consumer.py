#!/usr/bin/env python3

from json import loads, dumps

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from src.core.runner.manager import CaseManager
from src.core.utils.log import Logger
from src.db.crud import TaskCrud
from src.queue.defaults import DefaultValues as Default
from src.server.structures.task import TaskItem

logger = Logger.get_logger(name=__name__)


class Consumer:
    def __init__(
        self,
        host: str = Default.RABBITMQ_HOST,
        port: int = Default.RABBITMQ_PORT,
        task_queue: str = Default.TASK_QUEUE
    ):
        """
        Init rabbitmq consumer
        :param host: rabbitmq host
        :param port: rabbitmq port
        :param task_queue: queue name
        """
        self.connection = BlockingConnection(
            ConnectionParameters(host=host, port=port,)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=task_queue)
        self.channel.basic_consume(
            queue=task_queue,
            on_message_callback=self.task_process,
        )

        self.manager = CaseManager()

    def task_process(
        self,
        channel: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes
    ) -> None:
        """
        Process the received task
        :param channel: channel
        :param method: method
        :param properties: task properties
        :param body: task body
        :return: None
        """
        raw_body = loads(body.decode(encoding="utf-8"))
        cases = raw_body.get("cases", {})
        task = TaskItem(**raw_body.get("task", {}))

        try:
            results = list(self.manager.multi_case_runner(cases=cases))
            for result in results:
                TaskCrud.create_task_result(task, result or {})
            task.set_success(msg=f"Task done: {len(results)} out of {len(cases)} cases")
        except Exception as cases_err:
            task.set_error(msg=f"Task error: {str(cases_err)}")

        TaskCrud.update_task(task)
        logger.info(msg=f"Done task {task.task_id}")

        channel.basic_publish(
            exchange="",
            routing_key=properties.reply_to,
            properties=BasicProperties(correlation_id=properties.correlation_id),
            body=dumps(task.as_json()).encode(encoding="utf-8"),
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self) -> None:
        """
        Run consumer
        :return: None
        """
        self.channel.start_consuming()

    def __del__(self):
        """
        Force close connection
        :return: None
        """
        try:
            self.connection.close()
        except:
            pass
