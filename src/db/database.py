#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from os import environ


class DefaultValues:
    POSTGRES_DATABASE = environ.get("POSTGRES_DATABASE", default="osint")
    POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD", default="osint_framework")
    POSTGRES_USER = environ.get("POSTGRES_USER", default="osint_framework")
    POSTGRES_HOST = environ.get("POSTGRES_HOST", default="localhost")
    POSTGRES_PORT = environ.get("POSTGRES_PORT", default=str(5432))


Engine = create_engine(f"postgres+psycopg2://"
                       f"{DefaultValues.POSTGRES_USER}:{DefaultValues.POSTGRES_PASSWORD}@"
                       f"{DefaultValues.POSTGRES_HOST}:{DefaultValues.POSTGRES_PORT}/"
                       f"{DefaultValues.POSTGRES_DATABASE}")
if not database_exists(Engine.url):
    create_database(Engine.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

Base = declarative_base()
