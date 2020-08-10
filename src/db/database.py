#!/usr/bin/env python3

"""
Define basic values
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from os import environ


class DefaultValues:
    PG_DATABASE = environ.get("PG_DATABASE", default="osint")
    PG_PASSWORD = environ.get("PG_PASSWORD", default="osint_framework")
    PG_USER = environ.get("PG_USER", default="osint_framework")
    PG_HOST = environ.get("PG_HOST", default="localhost")
    PG_PORT = environ.get("PG_PORT", default=str(5432))


# Define engine, FIXME: required to get user+pass from environment
Engine = create_engine(
    f"postgres+psycopg2://"
    f"{DefaultValues.PG_USER}:{DefaultValues.PG_PASSWORD}@"
    f"{DefaultValues.PG_HOST}:{str(DefaultValues.PG_PORT)}/"
    f"{DefaultValues.PG_DATABASE}"
)
if not database_exists(Engine.url):
    create_database(Engine.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
Base = declarative_base()
