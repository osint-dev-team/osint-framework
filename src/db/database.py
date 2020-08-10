#!/usr/bin/env python3

"""
Define basic values
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


class DefaultValues:
    PG_USER = "osint_framework"
    PG_PASSWORD = "osint_framework"
    PG_HOST = "localhost"
    PG_PORT = 5432
    PG_DATABASE = "osint"


# Define engine, FIXME: required to get user+pass from environment
Engine = create_engine(f"postgres+psycopg2://"
                       f"{DefaultValues.PG_USER}:{DefaultValues.PG_PASSWORD}@"
                       f"{DefaultValues.PG_HOST}:{str(DefaultValues.PG_PORT)}/"
                       f"{DefaultValues.PG_DATABASE}")
if not database_exists(Engine.url):
    create_database(Engine.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
Base = declarative_base()
