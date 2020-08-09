#!/usr/bin/env python3

from multiprocessing import Process

from src.core.runner.manager import CaseManager
from src.db.crud import TaskCrud
from src.server.structures.task import TaskItem


class TaskSpawner:
    @staticmethod
    def process_task(task: TaskItem, case: dict, quantity: int) -> None:
        """
        Process single task in daemon process
        :param task: task object
        :param case: required data for searching
        :param quantity: quantity of tasks
        :return: None
        """
        case_manager = CaseManager()
        result = case_manager.single_case_runner(
            case_class=case.get("case"),
            case_name=case.get("name"),
            case_description=case.get("description"),
            *case.get("args", []),
            **case.get("kwargs", {})
        )
        TaskCrud.create_task_result(task, result)
        done_tasks = TaskCrud.get_results_count(task_id=task.task_id)
        if done_tasks == quantity:
            task.set_success(msg=f"All cases done")
        else:
            task.set_pending(msg=f"Done {done_tasks} of {quantity} cases")
        TaskCrud.update_task(task)

    @staticmethod
    def run_task(task: TaskItem, cases: dict) -> None:
        """
        Spawn task process
        :param task: task object
        :param cases: request body
        :return: None
        """
        quantity = len(cases)
        for case in cases:
            process = Process(
                target=TaskSpawner.process_task,
                kwargs={
                    "task": task,
                    "case": case,
                    "quantity": quantity
                },
                daemon=True
            )
            process.start()
        task.set_success(msg="Process spawning done")

        # How to detect if task is done?
        TaskCrud.update_task(task)
