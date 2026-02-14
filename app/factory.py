"""Factory function for User Repositories."""

import os

from dotenv import load_dotenv

from app.repository import InMemoryUserRepository, SQLiteUserRepository, UserRepository

load_dotenv()


def create_user_repository(repo_type: str | None = None) -> UserRepository:
    """Factory function to create the appropriate UserRepository."""
    if repo_type is None:
        repo_type = os.getenv("REPO_TYPE", "memory")

    repo_type = repo_type.lower()

    if repo_type == "memory":
        return InMemoryUserRepository()
    elif repo_type == "sqlite":
        return SQLiteUserRepository()
    else:
        raise ValueError(f"Unknown repository type: {repo_type}. Use 'memory' or 'sqlite'")
