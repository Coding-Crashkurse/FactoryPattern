"""FastAPI User Registration - Factory Pattern Demo."""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.factory import create_user_repository
from app.models import User, UserCreate
from app.repository import UserRepository

load_dotenv()
repo_type = os.getenv("REPO_TYPE", "memory")
repo: UserRepository = create_user_repository()



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    print(f"\n{'=' * 60}")
    print(f"FastAPI server started with: {repo_type.upper()} Repository")
    print(f"{'=' * 60}")
    print("\n[!] API is ready!")
    print(f"[*] Using: {repo.__class__.__name__}")
    print("[i] Tip: Change REPO_TYPE in .env to switch implementations\n")
    yield


app = FastAPI(
    title="User Registration API - Factory Pattern Demo",
    description="Demonstrates Factory Pattern with InMemory and SQLite repositories",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """Welcome endpoint with current repository info."""
    return {
        "message": "User Registration API - Factory Pattern Demo",
        "repository_type": repo_type,
        "endpoints": {
            "POST /users/": "Register new user",
            "GET /users/": "List all users",
            "GET /users/{user_id}": "Get specific user",
        },
    }


@app.post("/users/", response_model=User, status_code=201)
async def register_user(user_data: UserCreate):
    """Register a new user."""
    user = await repo.create_user(
        username=user_data.username,
        email=user_data.email,
    )
    return user


@app.get("/users/", response_model=list[User])
async def list_users():
    """List all registered users."""
    users = await repo.list_users()
    return users


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a specific user by ID."""
    user = await repo.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return user
