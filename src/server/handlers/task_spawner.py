#!/usr/bin/env python3

from multiprocessing import Process

from src.core.runner.manager import CaseManager
from src.db.crud import TaskCrud
from src.server.structures.task import TaskItem


class TaskSpawner:
    @staticmethod
    def process_task(task: TaskItem, case: dict) -> None:
        """
        Process single task in daemon process
        :param task: task object
        :param case: required data for searching
        :return: None
        """
        case_manager = CaseManager()
        try:
            result = case_manager.single_case_runner(
                case_class=case.get("case"),
                case_name=case.get("name"),
                case_description=case.get("description"),
                *case.get("args", []),
                **case.get("kwargs", {})
            )
        except Exception as unexp_err:
            pass
        else:
            TaskCrud.create_task_result(task, result)

    @staticmethod
    def run_task(task: TaskItem, cases: dict) -> None:
        """
        Spawn task process
        :param task: task object
        :param cases: request body
        :return: None
        """
        for case in cases:
            process = Process(
                target=TaskSpawner.process_task,
                kwargs={
                    "task": task,
                    "case": case
                },
                daemon=True
            )
            process.start()
        task.set_success(msg="Process spawning done")

        # How to detect if task is done?
        TaskCrud.update_task(task)
