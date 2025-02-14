import sqlalchemy as sqlal
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from dotenv import load_dotenv
import os

load_dotenv()

engine = sqlal.create_engine(os.getenv('POSTGRESQL_URL'))

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()
