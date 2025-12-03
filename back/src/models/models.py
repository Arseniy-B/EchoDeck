from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import ForeignKey
from datetime import datetime, timedelta
from enum import Enum
 

class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)


class TrackingStatus(Enum):
    RUNNING = "running"
    STOPPED = "stopped"


class Deck(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    tracking_status: Mapped[TrackingStatus] = mapped_column(nullable=False)


class Card(Base):
    deck_id: Mapped[int] = mapped_column(ForeignKey("deck.id"))
    question: Mapped[str] = mapped_column(nullable=False)
    answer: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)
    last_repetition_at: Mapped[datetime] = mapped_column(nullable=False)
    repetition_distance: Mapped[timedelta] = mapped_column(nullable=False)

