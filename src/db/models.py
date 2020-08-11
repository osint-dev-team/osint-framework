#!/usr/bin/env python3

from src.db.database import Base

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(String, unique=True, index=True, primary_key=True)
    status = Column(String)
    message = Column(String)
    datetime_start = Column(DateTime)
    datetime_finish = Column(DateTime)

    results = relationship("Result", back_populates="owner")


class Result(Base):
    __tablename__ = "results"

    result = Column(String)
    result_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(String, ForeignKey("tasks.task_id"))

    owner = relationship("Task", back_populates="results")
