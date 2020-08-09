#!/usr/bin/env python3

from sqlalchemy import Column, String

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
