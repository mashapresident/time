from sqlalchemy import Column, Integer, String, Boolean, or_, and_
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from db import db, Base

def init_db(engine):
    Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    password = Column(String(50), unique=True, nullable=False)
    
def check_user(username: str, password: str):
    with db.session() as session:
        user = session.query(Users).filter(
            (Users.name == username) & (Users.password == password)
        ).first()
        return user



class Record(Base):
    __tablename__ = "record"

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    priority = Column(Integer, nullable=False)
    date = Column(String, nullable=True)
    dayOfWeek = Column(String, nullable=True)
    filename = Column(String, nullable=False)
    time = Column(String, nullable=False)
    knockAfter = Column(Boolean, nullable=False)


def get_all_records() -> List[Dict]:
    with db.session() as session:
        records = session.query(Record).filter(Record.time.isnot(None)).order_by(Record.priority).all()
        return [
            {
                "id": record.id,
                "name": record.name,
                "priority": record.priority,
                "date": record.date,
                "dayOfWeek": record.dayOfWeek,
                "filename": record.filename,
                "time": record.time,
                "knockAfter": record.knockAfter,
            }
            for record in records
        ]


def add_record(new_event: dict):
    date_str = new_event.get("date")
    new_event["date"] = (
        datetime.strptime(date_str, "%Y-%m-%d").strftime("%d.%m.%Y")
        if date_str else None
    )

    new_event["dayOfWeek"] = new_event.get("dayOfWeek") or None

    time_str = new_event.get("time")
    new_event["time"] = (
        datetime.strptime(time_str, "%H:%M").strftime("%H:%M")
        if time_str else None
    )

    new_event["knockAfter"] = bool(new_event.get("knockAfter", False))

    record = Record(**new_event)
    with db.session() as session:
        session.add(record)
        session.commit()



def delete_record(record_id: int):
    with db.session() as session:
        record = session.get(Record, record_id)
        if record:
            session.delete(record)
            session.commit()


def get_filename(date_value: str, day_of_week: str, time_value: str) -> Tuple[Optional[str], Optional[bool]]:
    with db.session() as session:
        records = session.query(Record).filter(
            or_(
                and_(Record.date == date_value, Record.dayOfWeek.is_(None), Record.time == time_value),
                and_(Record.date.is_(None), Record.dayOfWeek == day_of_week, Record.time == time_value),
                and_(Record.date.is_(None), Record.dayOfWeek.is_(None), Record.time == time_value),
            )
        ).order_by(Record.priority).all()

        record = records[0] if records else None
        return (record.filename, record.knockAfter) if record else (None, None)