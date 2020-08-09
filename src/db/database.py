#!/usr/bin/env python3

"""
Define basic values
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

Engine = create_engine("postgres+psycopg2://admin1234:pass1234@localhost:5432/osint")
if not database_exists(Engine.url):
    create_database(Engine.url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
Base = declarative_base()
