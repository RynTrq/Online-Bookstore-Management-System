"""Runtime configuration for Shoponize."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DatabaseConfig:
    """Database connection settings loaded from environment variables."""

    backend: str = "sqlite"
    sqlite_path: Path = Path("shoponize.db")
    host: str = "127.0.0.1"
    port: int = 3306
    user: str = "root"
    password: str = ""
    database: str = "shoponize"

    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        backend = os.getenv("SHOPONIZE_DB_BACKEND", "sqlite").strip().lower()
        if backend not in {"sqlite", "mysql"}:
            raise ValueError("SHOPONIZE_DB_BACKEND must be either 'sqlite' or 'mysql'")

        port_text = os.getenv("SHOPONIZE_DB_PORT", "3306")
        try:
            port = int(port_text)
        except ValueError as exc:
            raise ValueError("SHOPONIZE_DB_PORT must be an integer") from exc

        return cls(
            backend=backend,
            sqlite_path=Path(os.getenv("SHOPONIZE_SQLITE_PATH", "shoponize.db")),
            host=os.getenv("SHOPONIZE_DB_HOST", "127.0.0.1"),
            port=port,
            user=os.getenv("SHOPONIZE_DB_USER", "root"),
            password=os.getenv("SHOPONIZE_DB_PASSWORD", ""),
            database=os.getenv("SHOPONIZE_DB_NAME", "shoponize"),
        )
