from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession
)
from asyncio import current_task
from src.config import config


class DBHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=5,
            max_overflow=10,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def get_session(self):
        async with self.session_factory() as session:
            yield session


db_helper = DBHelper(url=config.db.DATABASE_URL, echo=config.db.db_echo)
