#!/usr/bin/env python3

from multiprocessing import Process

from src.core.handlers.saver import Saver
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
            filename = Saver.save_results(result, name=str(task.task_id))
        except Exception as unexp_err:
            task.set_error(msg=str(unexp_err))
        else:
            task.set_success(msg=f"Successfully saved, filename: {filename}")
        finally:
            TaskCrud.update_task(task)

    @staticmethod
    def run_task(task: TaskItem, body: dict) -> None:
        """
        Spawn task process
        :param task: task object
        :param body: request body
        :return: None
        """
        process = Process(
            target=TaskSpawner.process_task,
            kwargs={
                "task": task,
                "case": body
            },
            daemon=True
        )
        process.start()
