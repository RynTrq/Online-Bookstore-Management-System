"""Small DB-API wrapper with SQLite and MySQL support."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator, Optional, Sequence

from .config import DatabaseConfig


class DatabaseError(RuntimeError):
    """Raised when a database operation cannot be completed."""


class Database:
    """A minimal database gateway used by the service layer."""

    def __init__(self, config: DatabaseConfig):
        self.config = config

    @contextmanager
    def connect(self) -> Iterator[Any]:
        connection = self._connect()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _connect(self) -> Any:
        if self.config.backend == "sqlite":
            if self.config.sqlite_path != Path(":memory:"):
                self.config.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
            connection = sqlite3.connect(str(self.config.sqlite_path))
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON")
            return connection

        try:
            import mysql.connector
        except ImportError as exc:
            raise DatabaseError(
                "mysql-connector-python is required when SHOPONIZE_DB_BACKEND=mysql"
            ) from exc

        return mysql.connector.connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.user,
            password=self.config.password,
            database=self.config.database,
        )

    def sql(self, query: str) -> str:
        if self.config.backend == "mysql":
            return query.replace("?", "%s")
        return query

    def execute(self, connection: Any, query: str, params: Sequence[Any] = ()) -> Any:
        cursor = connection.cursor()
        cursor.execute(self.sql(query), tuple(params))
        return cursor

    def scalar(
        self, connection: Any, query: str, params: Sequence[Any] = ()
    ) -> Optional[Any]:
        row = self.execute(connection, query, params).fetchone()
        if row is None:
            return None
        return row[0]

    def row(
        self, connection: Any, query: str, params: Sequence[Any] = ()
    ) -> Optional[Any]:
        return self.execute(connection, query, params).fetchone()

    def rows(
        self, connection: Any, query: str, params: Sequence[Any] = ()
    ) -> Iterable[Any]:
        return self.execute(connection, query, params).fetchall()
