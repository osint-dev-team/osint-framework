#!/usr/bin/env python3

from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.db.database import Base


class Task(Base):
    """
    Defines basic task structure
    """

    __tablename__ = "tasks"

    task_id = Column(String, unique=True, index=True, primary_key=True)
    status = Column(String)
    message = Column(String)
    datetime_start = Column(String)
    datetime_finish = Column(String)

    results = relationship("Result", back_populates="owner")


class Result(Base):
    """
    Defines results
    """

    __tablename__ = "results"

    result = Column(String)
    result_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(String, ForeignKey("tasks.task_id"))

    owner = relationship("Task", back_populates="results")
