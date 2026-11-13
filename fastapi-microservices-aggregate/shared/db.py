"""Database connection and session lifecycle management."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

__all__ = ["Base", "DatabaseManager"]


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy declarative models."""


class DatabaseManager:
    """Manages an async SQLAlchemy engine and session factory."""

    def __init__(self, db_url: str, echo: bool = False) -> None:
        self.db_url = db_url
        engine_kwargs: dict[str, object] = {"echo": echo}
        if "sqlite" in db_url:
            # SQLite does not support standard connection pool sizing
            engine_kwargs["connect_args"] = {"check_same_thread": False}
        else:
            engine_kwargs["pool_pre_ping"] = True
            engine_kwargs["pool_size"] = 10
            engine_kwargs["max_overflow"] = 20

        self.engine: AsyncEngine = create_async_engine(db_url, **engine_kwargs)
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    async def init_tables(self) -> None:
        """Creates all registered tables if they do not exist."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def close(self) -> None:
        """Disposes the underlying connection pool."""
        await self.engine.dispose()

    async def health_check(self) -> bool:
        """Executes a simple SELECT 1 to verify database connectivity."""
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Context manager providing an active transactional session."""
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """FastAPI dependency for injecting an async database session."""
        async with self.session() as session:
            yield session
