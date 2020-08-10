#!/usr/bin/env python3

"""
Tornado-based server with REST API support
"""

from abc import ABC
from logging import DEBUG
from typing import Any

import tornado.log
from tornado import httputil
from tornado.escape import json_decode, json_encode
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line
from tornado.web import RequestHandler, Application

from src.db.crud import TaskCrud
from src.db.database import Engine, Base
from src.server.handlers.task_spawner import TaskSpawner
from src.server.structures.response import ServerResponse
from src.server.structures.task import TaskItem

# Set logging level for Tornado Server
tornado.log.access_log.setLevel(DEBUG)

# Define our logger
logger = tornado.log.app_log


class BaseHandler(RequestHandler, ABC):
    """
    Add basic handler to support 'success', 'error'
    messages and more
    """

    def __init__(
        self,
        application: "Application",
        request: httputil.HTTPServerRequest,
        **kwargs: Any,
    ):
        super().__init__(application, request, **kwargs)
        self.server_response = ServerResponse()

    def set_default_headers(self) -> None:
        """
        Set default header to 'application/json' because of
        the endpoint nature (JSON-based response)
        :return: None
        """
        self.set_header("Content-Type", "application/json")

    def success(self, msg: str = "") -> None:
        """
        Return success status
        :param msg: additional message
        :return: None
        """
        self.set_status(status_code=200)
        response = self.server_response.success(msg=msg)
        self.write(response)

    def error(self, msg: str = "") -> None:
        """
        Return error status
        :param msg: additional message
        :return: None
        """
        self.set_status(status_code=500)
        response = self.server_response.error(msg=msg)
        self.write(response)


class CreateTaskHandler(BaseHandler, ABC):
    """
    Create basic task handler
    """

    def post(self):
        """
        Handle task create process
        :return: task object
        """
        try:
            body = json_decode(self.request.body)
            task = TaskItem()
            TaskCrud.create_task(task=task)
            TaskSpawner().run_task(task, body)
            response = json_encode(task.as_json())
        except Exception as create_task_err:
            return self.error(
                msg=f"Unexpected error at task creating: {str(create_task_err)}"
            )
        self.write(response)


class ListTaskHandler(BaseHandler, ABC):
    """
    Return tasks
    """

    def get(self) -> None:
        """
        Return tasks data
        :return: None
        """
        try:
            task_id = self.get_argument("task_id", None)
            tasks = json_encode(
                TaskCrud.get_task(task_id) if task_id else TaskCrud.get_tasks()
            )
        except Exception as list_task_err:
            return self.error(
                msg=f"Unexpected error at tasks listing: {str(list_task_err)}"
            )
        self.write(tasks)


class ResultsHandler(BaseHandler, ABC):
    """
    Return results
    """

    def get(self) -> None:
        """
        Return results data
        :return: None
        """
        try:
            task_id = self.get_argument("task_id", None)
            results = json_encode(TaskCrud.get_results(task_id))
        except Exception as get_results_error:
            return self.error(
                msg=f"Unexpected error at getting results: {str(get_results_error)}"
            )
        self.write(results)


def make_app() -> Application:
    """
    Create application
    :return: Application
    """
    return Application(
        handlers=[
            (r"/api/tasks/create", CreateTaskHandler),
            (r"/api/tasks/list", ListTaskHandler),
            (r"/api/results", ResultsHandler),
        ]
    )


if __name__ == "__main__":
    # Enable logging
    parse_command_line()

    # Prepare database
    Base.metadata.create_all(Engine)

    # Create application
    app = make_app()
    app.listen(port=8888)

    # Here we go!
    logger.info(msg="Server successfully started. Wait for incoming connections.")
    IOLoop.current().start()
