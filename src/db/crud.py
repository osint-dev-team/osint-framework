#!/usr/bin/env python3

from sqlalchemy import inspect, desc
from sqlalchemy.orm import Session
from json import dumps, loads

from src.db import models
from src.db.database import SessionLocal
from src.server.structures.task import TaskItem


def object_as_dict(obj):
    """
    Defines object mapper for database raw results
    see: https://riptutorial.com/sqlalchemy/example/6614/converting-a-query-result-to-dict
    :param obj: object to wrap
    :return: dictionary representing database results
    """
    if not obj:
        return obj
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


class TaskCrud:
    """
    Defines namespace 'TaskCrud' to use different database handlers
    """

    @staticmethod
    def create_task(task: TaskItem, db: Session = SessionLocal()) -> None:
        """
        Create task in database
        :param task: 'TaskItem' object
        :param db: database to use
        :return: None
        """
        try:
            db_task = models.Task(**dict(task))
            db.add(db_task)
            db.commit()
        except:
            db.rollback()
        finally:
            db.close()

    @staticmethod
    def create_task_result(
        task: TaskItem, result: dict or list, db: Session = SessionLocal()
    ) -> None:
        """
        Create result for task
        :param task:
        :param result:
        :param db:
        :return:
        """
        try:
            db_result = models.Result(
                result=dumps(result, default=str), owner_id=task.task_id
            )
            db.add(db_result)
            db.commit()
        except:
            db.rollback()
        db.close()

    @staticmethod
    def update_task(task: TaskItem, db: Session = SessionLocal()) -> None:
        """
        Update task in database
        :param task: 'TaskItem' object
        :param db: database to use
        :return: None
        """
        try:
            db.query(models.Task).filter_by(task_id=task.task_id).update(dict(task))
            db.commit()
        except:
            db.rollback()
        finally:
            db.close()

    @staticmethod
    def get_results(task_id: str, db: Session = SessionLocal()) -> list:
        """
        Return results
        :param task_id: task id to use
        :param db: database to use
        :return: dict
        """
        try:
            results = (
                db.query(models.Result).filter(models.Result.owner_id == task_id).all()
            )
        except:
            return []
        else:
            return [loads(str(data.result)) for data in results]
        finally:
            db.close()

    @staticmethod
    def get_results_count(task_id: str, db: Session = SessionLocal()) -> int:
        """
        Return resutls count
        :param task_id: task id to use
        :param db: database to use
        :return: counter
        """
        try:
            return (
                db.query(models.Result)
                .filter(models.Result.owner_id == task_id)
                .count()
            )
        except:
            return 0
        finally:
            db.close()

    @staticmethod
    def get_task(task_id: str, db: Session = SessionLocal()) -> dict:
        """
        Return task results by UUID
        :param task_id: task id to use
        :param db: database to use
        :return: dict
        """
        try:
            result = db.query(models.Task).filter_by(task_id=task_id).first()
        except:
            return {}
        else:
            return object_as_dict(result)
        finally:
            db.close()

    @staticmethod
    def get_tasks(limit: int, db: Session = SessionLocal()) -> list:
        """
        Return all tasks
        :param limit: limit of results
        :param db: database to use
        :return: list of results
        """
        try:
            results = db.query(models.Task).order_by(desc(models.Task.datetime_start)).limit(limit).all()
        except:
            # FIXME: This exception can be possible IMMEDIATELY after task creation. Fixes?
            return []
        else:
            return [object_as_dict(result) for result in results]
        finally:
            db.close()
