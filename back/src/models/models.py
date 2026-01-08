from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import ForeignKey
from datetime import datetime
from enum import Enum


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class User(Base):
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    disabled: Mapped[bool] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)


class Status(Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class Collection(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    title: Mapped[str]
    descrdiption: Mapped[str]
    status: Mapped[Status]


class Note(Base):
    collection_id: Mapped[int] = mapped_column(ForeignKey("collection.id"), index=True)
    image: Mapped[str]
    sound: Mapped[str]
    sound_meaning: Mapped[str]
    sound_example: Mapped[str]
    meaning: Mapped[str]
    example: Mapped[str]


class Deck(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)


class Card(Base):
    deck_id: Mapped[int] = mapped_column(ForeignKey("deck.id"), index=True)
    note_id: Mapped[int] = mapped_column(ForeignKey("note.id"), index=True)
    last_repeat: Mapped[datetime]
    ease_factor: Mapped[int]
