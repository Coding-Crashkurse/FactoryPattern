"""User Repository - ABC Interface with InMemory and SQLite implementations."""

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy import select

from app.db import Base, UserModel, get_async_engine, get_session_maker
from app.models import User


class UserRepository(ABC):
    """Abstract base class for all User Repository implementations."""

    @abstractmethod
    async def create_user(self, username: str, email: str) -> User:
        pass

    @abstractmethod
    async def get_user(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def list_users(self) -> list[User]:
        pass


class InMemoryUserRepository(UserRepository):
    """In-memory user storage."""

    def __init__(self):
        self._users: dict[int, User] = {}
        self._next_id: int = 1
        self._lock = asyncio.Lock()
        print("[OK] InMemoryUserRepository initialized")

    async def create_user(self, username: str, email: str) -> User:
        async with self._lock:
            user = User(
                id=self._next_id,
                username=username,
                email=email,
                created_at=datetime.now(),
            )
            self._users[user.id] = user
            self._next_id += 1
            print(f"  > Created user (memory): {user.username} (ID: {user.id})")
            return user

    async def get_user(self, user_id: int) -> User | None:
        user = self._users.get(user_id)
        print(f"  > Get user (memory): ID {user_id} > {user.username if user else 'Not found'}")
        return user

    async def list_users(self) -> list[User]:
        users = list(self._users.values())
        print(f"  > Listed {len(users)} user(s) from memory")
        return users


class SQLiteUserRepository(UserRepository):
    """SQLite database user storage using SQLAlchemy ORM."""

    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self.session_maker = get_session_maker(db_path)
        self._initialized = False
        print(f"[OK] SQLiteUserRepository initialized (DB: {db_path})")

    async def _init_db(self):
        if self._initialized:
            return

        engine = get_async_engine(self.db_path)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        self._initialized = True

    async def create_user(self, username: str, email: str) -> User:
        await self._init_db()

        async with self.session_maker() as session:
            db_user = UserModel(username=username, email=email)
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)

            user = User.model_validate(db_user)
            print(f"  > Created user (SQLite): {user.username} (ID: {user.id})")
            return user

    async def get_user(self, user_id: int) -> User | None:
        await self._init_db()

        async with self.session_maker() as session:
            result = await session.execute(select(UserModel).where(UserModel.id == user_id))
            db_user = result.scalar_one_or_none()

            if db_user:
                user = User.model_validate(db_user)
                print(f"  > Get user (SQLite): ID {user_id} > {user.username}")
                return user

        print(f"  > User not found (SQLite): ID {user_id}")
        return None

    async def list_users(self) -> list[User]:
        await self._init_db()

        async with self.session_maker() as session:
            result = await session.execute(select(UserModel).order_by(UserModel.id))
            db_users = result.scalars().all()

            users = [User.model_validate(db_user) for db_user in db_users]

        print(f"  > Listed {len(users)} user(s) from SQLite")
        return users
