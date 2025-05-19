from typing import List, Dict, Optional
from sqlalchemy import String, Date, Time, Boolean, and_, select, Integer
from sqlalchemy.orm import Mapped, mapped_column
import os
from db import Base, engine, async_session
from datetime import *


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[Optional[str]] = mapped_column(Date)
    dayOfWeek: Mapped[Optional[str]] = mapped_column(String)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    time: Mapped[str] = mapped_column(Time, nullable=False)
    knockAfter: Mapped[bool] = mapped_column(Boolean, nullable=False)


async def init_db():
    if not os.path.exists("Record.db"):
        print("База не існує. Створюємо нову...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Базу та таблиці ініціалізовано")


async def get_all_records() -> List[Dict]:
    async with async_session() as session:
        result = await session.execute(
            select(Record)
            .where(
                Record.time.is_not(None)
            )
            .order_by(Record.priority)
        )
        records = result.scalars().all()
        return [
            {
                "id": record.id,
                "name": record.name,
                "priority": record.priority,
                "date": record.date.isoformat() if record.date else None,
                "dayOfWeek": record.dayOfWeek,
                "filename": record.filename,
                "time": record.time.isoformat() if record.time else None,
                "knockAfter": record.knockAfter,
            }
            for record in records
        ]


async def add_record(new_event: dict):
    # Обробка поля date
    date_str = new_event.get("date")
    if date_str:
        try:
            new_event["date"] = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            new_event["date"] = None
    else:
        new_event["date"] = None

    # Обробка поля time
    time_str = new_event.get("time")
    if time_str:
        try:
            new_event["time"] = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            new_event["time"] = None
    else:
        new_event["time"] = None
    new_event["knockAfter"] = bool(new_event.get("knockAfter", False))

    async with async_session() as session:
        record = Record(**new_event)
        session.add(record)
        await session.commit()
        print("Запис додано успішно")


async def delete(record_id: int):
    async with async_session() as session:
        record = await session.get(Record, record_id)
        if record:
            await session.delete(record)
            await session.commit()
            print(f"Запис з id={record_id} успішно видалено")
        else:
            print(f"Запис з id={record_id} не знайдено")


async def get_filename(date: date, day_of_week: str, time: time) -> tuple[Optional[str], Optional[bool]]:
    async with async_session() as session:
        filters = [
            Record.date == date,
            Record.dayOfWeek == day_of_week,
            Record.time == time
        ]
        stmt = (
            select(Record)
            .where(and_(*filters))
            .order_by(Record.priority)
        )
        result = await session.execute(stmt)
        record = result.scalars().first()

        print(record.filename if record else "Запис не знайдено")
        return (record.filename, record.knockAfter) if record else (None, None)