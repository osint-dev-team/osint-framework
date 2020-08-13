#!/usr/bin/env python3

from src.server.structures.task import TaskItem
from src.db.database import SessionLocal, Base, Engine
from src.db import models
from sqlalchemy.orm import Session
from sqlalchemy import inspect, desc
from json import dumps, loads
from pprint import pprint


def object_as_dict(object):
    if not object:
        return object
    return {c.key: getattr(object, c.key) for c in inspect(object).mapper.column_attrs}


class TaskCrud:
    @staticmethod
    def create_result(task: TaskItem, result: dict or list, db: Session = SessionLocal()) -> None:
        db_result = models.Result(result=dumps(result, default=str), owner_id=task.task_id)
        db.add(db_result)
        db.commit()
        db.close()

    @staticmethod
    def get_results(task_id: str, db: Session = SessionLocal()) -> list:
        results = db.query(models.Result).filter(models.Result.owner_id == task_id).all()
        db.close()
        return [loads(str(data.result)) for data in results]

    @staticmethod
    def get_results_count(task_id: str, db: Session = SessionLocal()) -> int:
        count = db.query(models.Result).filter(models.Result.owner_id == task_id).count()
        db.close()
        return count

    @staticmethod
    def create_task(task: TaskItem, db: Session = SessionLocal()) -> None:
        db_task = models.Task(**dict(task))
        db.add(db_task)
        db.commit()
        db.close()

    @staticmethod
    def update_task(task: TaskItem, db: Session = SessionLocal()) -> None:
        db.query(models.Task).filter_by(task_id=task.task_id).update(dict(task))
        db.commit()
        db.close()

    @staticmethod
    def get_task(task_id: str, db: Session = SessionLocal()) -> dict:
        task_result = db.query(models.Task).filter_by(task_id=task_id).first()
        db.close()
        return object_as_dict(task_result)

    @staticmethod
    def get_tasks(limit: int, db: Session = SessionLocal()) -> list:
        ret_tasks = []
        try:
            tasks = db.query(models.Task).order_by(desc(models.Task.datetime_start)).limit(limit).all()
        except:
            pass
        else:
            ret_tasks = [object_as_dict(task_result) for task_result in tasks]
        finally:
            db.close()
            return ret_tasks


if __name__ == "__main__":
    Base.metadata.create_all(Engine)

    task = TaskItem()
    TaskCrud.create_task(task)

    task.set_success(msg="Successfully done")
    TaskCrud.update_task(task)

    # pprint(TaskCrud.get_tasks(limit=10))

    TaskCrud.create_result(task, result={"hello": "world"})
    TaskCrud.create_result(task, result={"hello": "world"})
    TaskCrud.create_result(task, result={"hello": "world"})

    task_id = task.task_id

    print(TaskCrud.get_results(task_id=task_id))
    print(TaskCrud.get_results_count(task_id=task_id))
