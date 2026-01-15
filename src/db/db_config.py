# from sqlmodel import Session as SqlModelSession, create_engine as sqlmodel_create_engine
import os
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")


# sqlmodel_engine = sqlmodel_create_engine(DATABASE_URL, echo=True)
# session = SqlModelSession(sqlmodel_engine)


engine = create_engine(DATABASE_URL, echo=True)


Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
