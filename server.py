#!/usr/bin/env python3

from abc import ABC

from tornado.web import RequestHandler, Application
from tornado.escape import json_decode, json_encode
from tornado import httputil
from tornado.ioloop import IOLoop
from typing import Any
from multiprocessing import Process

from src.server.structures.task import TaskItem
from src.core.runner.manager import CaseManager
from main import save_results


class BaseHandler(RequestHandler, ABC):
    def __init__(self, application: "Application", request: httputil.HTTPServerRequest, **kwargs: Any):
        super().__init__(application, request, **kwargs)

    def set_default_headers(self) -> None:
        self.set_header("Content-Type", "application/json")

    def success(self, msg: str or Any = "") -> None:
        self.set_status(status_code=200)
        response = {"status": "success", "message": str(msg)}
        return self.write(response)

    def error(self, msg: str or Any = "") -> None:
        self.set_status(status_code=500)
        response = {"status": "error", "message": str(msg)}
        return self.write(response)


class TaskSpawner:
    @staticmethod
    def process_task(task: TaskItem, case: dict) -> None:
        manager = CaseManager()
        result = manager.single_case_runner(
            case_class=case.get("case"),
            case_name=case.get("name"),
            case_description=case.get("description"),
            *case.get("args", []),
            **case.get("kwargs", {})
        )
        save_results(results=result)

    @staticmethod
    def run_task(task: TaskItem, case: dict) -> None:
        process = Process(
            target=TaskSpawner.process_task,
            kwargs={
                "task": task,
                "case": case
            },
            daemon=True
        )
        process.start()
        task.set_success()


class CreateTaskHandler(BaseHandler, ABC):
    def post(self):
        body = json_decode(self.request.body)
        task = TaskItem()
        TaskSpawner.run_task(task, case=body)
        response = json_encode(task.as_json())
        return self.write(response)

    def get(self):
        self.error(msg="Only POST method are allowed")


class ListTaskHandler(BaseHandler, ABC):
    def get(self):
        task_id = self.get_argument("task_id", None)
        ...
        return self.success(msg=f"Task id is: {task_id}")


class ResultsHandler(BaseHandler, ABC):
    def get(self):
        ...


def make_app() -> Application:
    return Application(
        handlers=[
            (r"/api/tasks/create", CreateTaskHandler),
            (r"/api/tasks/list", ListTaskHandler),
            (r"/api/results", ResultsHandler)
        ]
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(port=8888)

    IOLoop.current().start()
