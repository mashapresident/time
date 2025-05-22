from sqlalchemy import *
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(Integer, nullable=False)

