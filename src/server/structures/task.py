#!/usr/bin/env python3

from datetime import datetime
from uuid import uuid4


class DefaultValues:
    EMPTY = ""


class TaskStatus:
    PENDING = "pending"
    SUCCESS = "success"
    ERROR = "error"


class TaskItem:
    def __init__(
        self,
        status: str = TaskStatus.PENDING,
        message: str = DefaultValues.EMPTY,
        task_id: uuid4 = uuid4,
        datetime_start: datetime or None = None,
        datetime_finish: datetime or None = None
    ):
        self.status = status
        self.message = message
        self.task_id = str(task_id())
        self.datetime_start = datetime_start if datetime_start else datetime.now()
        self.datetime_finish = datetime_finish

    def __repr__(self) -> str:
        return f"Task item, instance of the class '{self.__class__.__name__}'. Values: " \
               f"'status'='{self.status}', " \
               f"'message'='{self.message}', " \
               f"'task_id'='{self.task_id}', " \
               f"'datetime_start'='{self.datetime_start}', " \
               f"'datetime_finish'='{self.datetime_finish}'"

    def __iter__(self) -> iter:
        return iter(list(vars(self).items()))

    def set_success(self, msg: str = DefaultValues.EMPTY) -> None:
        self.status = TaskStatus.SUCCESS
        self.datetime_finish = datetime.now()
        self.message = msg

    def set_error(self, msg: str = DefaultValues.EMPTY) -> None:
        self.status = TaskStatus.ERROR
        self.datetime_finish = datetime.now()
        self.message = msg

    def set_pending(self, msg: str = DefaultValues.EMPTY) -> None:
        self.status = TaskStatus.PENDING
        self.message = msg

    def as_json(self) -> dict:
        return {key: str(value) if value else value for (key, value) in vars(self).items()}
