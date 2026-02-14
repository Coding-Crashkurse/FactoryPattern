"""SQLAlchemy database models and setup."""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    """SQLAlchemy User model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


def get_async_engine(db_path: str = "users.db"):
    """Create async SQLite engine."""
    return create_async_engine(f"sqlite+aiosqlite:///{db_path}", echo=False)


def get_session_maker(db_path: str = "users.db") -> async_sessionmaker[AsyncSession]:
    """Create async session maker."""
    engine = get_async_engine(db_path)
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
