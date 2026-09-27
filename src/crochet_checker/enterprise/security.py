"""Security helpers for the enterprise API."""

from __future__ import annotations

import os
import time
from collections import defaultdict, deque

from fastapi import Header, HTTPException


class RateLimiter:
    """Simple process-local sliding-window limiter."""

    def __init__(
        self,
        max_requests: int = 60,
        window_seconds: int = 60,
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, deque[float]] = defaultdict(deque)

    def check(self, identity: str) -> None:
        now = time.monotonic()
        history = self.requests[identity]

        while history and now - history[0] > self.window_seconds:
            history.popleft()

        if len(history) >= self.max_requests:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again later.",
            )

        history.append(now)


def require_api_key(
    x_api_key: str | None = Header(default=None),
) -> str:
    """
    Require X-API-Key only when CROCHET_API_KEY is configured.

    Leaving CROCHET_API_KEY unset keeps local development convenient.
    Production deployments should always configure it.
    """
    expected = os.environ.get("CROCHET_API_KEY")

    if not expected:
        return "development"

    if not x_api_key or x_api_key != expected:
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid API key.",
        )

    return "authenticated"
