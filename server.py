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
from json import dumps

from src.db.database import Base, Engine
from src.db.crud import TaskCrud


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
    def process_task(task: TaskItem, case: dict, cases_len: int) -> None:
        Engine.dispose()
        manager = CaseManager()
        result = manager.single_case_runner(
            case_class=case.get("case"),
            case_name=case.get("name"),
            case_description=case.get("description"),
            *case.get("args", []),
            **case.get("kwargs", {})
        )
        TaskCrud.create_result(task, result=result)

        done_cases = TaskCrud.get_results_count(task_id=task.task_id)

        if done_cases == cases_len:
            task.set_success(msg=f"All cases done ({done_cases} out of {cases_len})")
        else:
            task.set_pending(msg=f"Done {done_cases} out of {cases_len} cases")

        TaskCrud.update_task(task)

    @staticmethod
    def run_task(task: TaskItem, cases: list) -> None:
        cases_len = len(cases)
        for case in cases:
            process = Process(
                target=TaskSpawner.process_task,
                kwargs={
                    "task": task,
                    "case": case,
                    "cases_len": cases_len,
                },
                daemon=True
            )
            process.start()


class CreateTaskHandler(BaseHandler, ABC):
    def post(self):
        body = json_decode(self.request.body)
        task = TaskItem()
        TaskCrud.create_task(task)
        TaskSpawner.run_task(task, cases=body)
        response = json_encode(task.as_json())
        return self.write(response)

    def get(self):
        self.error(msg="Only POST method are allowed")


class ListTaskHandler(BaseHandler, ABC):
    def get(self):
        task_id = self.get_argument("task_id", None)
        limit = self.get_argument("limit", None)

        tasks = dumps(
            TaskCrud.get_task(task_id)
            if task_id
            else TaskCrud.get_tasks(int(limit) if limit else None), default=str
        )

        self.write(tasks)


class ResultsHandler(BaseHandler, ABC):
    def get(self):
        task_id = self.get_argument("task_id", None)
        results = json_encode(TaskCrud.get_results(task_id))

        self.write(results)


class HealthCheckHandler(BaseHandler, ABC):
    def get(self):
        self.write({"status": "up"})


def make_app() -> Application:
    return Application(
        handlers=[
            (r"/api/tasks/create", CreateTaskHandler),
            (r"/api/tasks/list", ListTaskHandler),
            (r"/api/results", ResultsHandler),
            (r"/api/health", HealthCheckHandler),
        ]
    )


if __name__ == "__main__":
    Base.metadata.create_all(Engine)

    app = make_app()
    app.listen(port=8888)

    IOLoop.current().start()
