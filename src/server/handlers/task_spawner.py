#!/usr/bin/env python3

from multiprocessing import Process

from src.core.runner.manager import CaseManager
from src.db.crud import TaskCrud
from src.db.database import Engine
from src.server.structures.task import TaskItem


class TaskSpawner:
    @staticmethod
    def process_task(task: TaskItem, case: dict, cases_len: int) -> None:
        """
        Process single task in daemon process
        :param task: task object
        :param case: required data for searching
        :param cases_len: quantity of tasks
        :return: None
        """
        # see:
        # https://stackoverflow.com/questions/30241911/psycopg2-error-databaseerror-error-with-no-message-from-the-libpq
        Engine.dispose()
        case_manager = CaseManager()
        result = case_manager.single_case_runner(
            case_class=case.get("case"),
            case_name=case.get("name"),
            case_description=case.get("description"),
            *case.get("args", []),
            **case.get("kwargs", {}),
        )
        # Save results to database
        TaskCrud.create_task_result(task, result or {})

        # Count quantity of done cases for particular id
        done_tasks = TaskCrud.get_results_count(task_id=task.task_id)

        if done_tasks == cases_len:
            task.set_success(msg=f"All cases done ({done_tasks} out of {cases_len})")
        else:
            task.set_pending(msg=f"Done {done_tasks} out of {cases_len} cases")

        # Update task in any case
        TaskCrud.update_task(task)

    @staticmethod
    def run_task(task: TaskItem, cases: dict) -> None:
        """
        Spawn task process
        :param task: task object
        :param cases: request body
        :return: None
        """
        cases_len = len(cases)
        for case in cases:
            Process(
                target=TaskSpawner.process_task,
                kwargs={"task": task, "case": case, "cases_len": cases_len},
                daemon=True,
            ).start()
