from sqlmodel import Session, create_engine
import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

engine = create_engine(DATABASE_URL, echo=True)
session = Session(engine)
