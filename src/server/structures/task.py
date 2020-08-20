#!/usr/bin/env python3

from datetime import datetime
from typing import Union
from uuid import uuid4


class DefaultValues:
    """
    Define some default values
    """

    EMPTY = ""


class TaskStatus:
    """
    Define basic statuses for the task
    """

    PENDING = "pending"
    SUCCESS = "success"
    ERROR = "error"


class TaskItem:
    """
    Implement basic task structure
    """

    def __init__(
        self,
        status: str = TaskStatus.PENDING,
        message: str = DefaultValues.EMPTY,
        task_id: Union[uuid4, str] = uuid4,
        datetime_start: Union[datetime, str, None] = None,
        datetime_finish: Union[datetime, str, None] = None,
    ):
        """
        Define basic structure
        :param status: status of the current task, can be 'pending', 'success', 'error'.
            By default set to 'unknown' (because we don't know if the task is started yet or not)
        :param message: message with the additional information.
            By default set to '""', because this message is not really required.
        :param task_id: UUID of the task.
            By default generates new UUID every time with the initialization.
        :param datetime_start: Start time of the task.
            By default set to the creation process of the task.
        :param datetime_finish: Finish time of the task.
            By default is set to 'None', because task can be unfinished.
        """
        self.status = status
        self.message = message
        self.task_id = str(task_id()) if not isinstance(task_id, str) else task_id
        self.datetime_start = datetime.strptime(
            datetime_start, "%Y-%m-%d %H:%M:%S.%f"
        ) if isinstance(datetime_start, str) else datetime.now()
        self.datetime_finish = datetime.strptime(
            datetime_finish, "%Y-%m-%d %H:%M:%S.%f"
        ) if isinstance(datetime_finish, str) else datetime_finish

    def __repr__(self) -> str:
        """
        Implement printable representation
        :return: string with representation
        """
        return (
            f"Task item, instance of the class '{self.__class__.__name__}'. "
            f"Values: "
            f"'status'='{self.status}', "
            f"'message'='{self.message}', "
            f"'task_id'='{self.task_id}', "
            f"'datetime_start'='{self.datetime_start}', "
            f"'datetime_finish'='{self.datetime_finish}'"
        )

    def __iter__(self) -> iter:
        """
        Implement iterable representation for casting
        :return: iterable
        """
        return iter(list(vars(self).items()))

    def set_success(self, msg: str) -> None:
        """
        Define success completion
        :param msg: additional info
        :return: None
        """
        self.status = TaskStatus.SUCCESS
        self.datetime_finish = datetime.now()
        self.message = msg

    def set_error(self, msg: str) -> None:
        """
        Define error completion
        :param msg: additional info
        :return: None
        """
        self.status = TaskStatus.ERROR
        self.datetime_finish = datetime.now()
        self.message = msg

    def set_pending(self, msg: str) -> None:
        """
        Define pending status
        :param msg: additional info
        :return: None
        """
        self.status = TaskStatus.PENDING
        self.message = msg

    def as_json(self) -> dict:
        """
        Implement str cast representation to dump data
        :return: dict with str-repr data
        """
        return {
            key: str(value) if value else value for (key, value) in vars(self).items()
        }
