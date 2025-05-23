from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

engine = create_engine("sqlite:///database.db", echo=False)

Base = declarative_base()

class DB:
    def session(self):
        return Session(bind=engine)

db = DB()
