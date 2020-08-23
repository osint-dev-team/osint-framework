#!/usr/bin/env python3

from json import loads, dumps

import pika

from src.core.runner.manager import CaseManager
from src.core.utils.log import Logger
from src.db.crud import TaskCrud
from src.queue.defaults import DefaultValues as Default
from src.server.structures.task import TaskItem

logger = Logger.get_logger(name=__name__)


class Consumer:
    def __init__(
        self, host: str = Default.RABBITMQ_HOST, port: int = Default.RABBITMQ_PORT
    ):
        """
        Init rabbitmq consumer
        :param host: rabbitmq host
        :param port: rabbitmq port
        """
        self.queue = Default.QUEUE
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port,)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        self.manager = CaseManager()

    def callback(self, ch, method, properties, body) -> None:
        """
        Process the received task
        :param ch: channel
        :param method: method
        :param properties: task properties
        :param body: task body
        :return: None
        """
        raw_body = loads(body)
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

        ch.basic_publish(
            exchange="",
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=dumps(task.as_json()),
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self) -> None:
        """
        Run consumer
        :return: None
        """
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback)
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
