"""Password hashing and verification helpers."""

from __future__ import annotations

import hashlib
import hmac
import os
from typing import Optional


HASH_PREFIX = "sha256"


def hash_password(password: str, salt: Optional[str] = None) -> str:
    """Return a salted SHA-256 password hash suitable for this local project."""

    if salt is None:
        salt = os.urandom(16).hex()
    digest = hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()
    return f"{HASH_PREFIX}${salt}${digest}"


def verify_password(candidate: str, stored_password: str) -> bool:
    """Verify hashed passwords while retaining compatibility with seed data."""

    if stored_password.startswith(f"{HASH_PREFIX}$"):
        try:
            _, salt, expected = stored_password.split("$", 2)
        except ValueError:
            return False
        actual = hash_password(candidate, salt).split("$", 2)[2]
        return hmac.compare_digest(actual, expected)

    return hmac.compare_digest(candidate, stored_password)
