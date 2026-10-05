"""Typed TypeSafe/Jev adapter. No chat generation and no clinical profile payloads."""
import asyncio
import logging
import os
from functools import lru_cache

from typesafe_sdk import AsyncTypeSafeClient, RetryPolicy, TypeSafeAPIError

logger = logging.getLogger(__name__)
_serial = asyncio.Semaphore(1)


@lru_cache(maxsize=1)
def get_jev_client() -> AsyncTypeSafeClient:
    return AsyncTypeSafeClient(
        api_key=os.environ["EMERGENT_LLM_KEY"],
        base_url=os.environ["INTEGRATION_PROXY_URL"].rstrip("/") + "/llm/typesafe",
        retry=RetryPolicy(max_retries=2, respect_retry_after=False), timeout=4,
    )


def jev_error_code(exc: Exception) -> str:
    if not isinstance(exc, TypeSafeAPIError):
        return "unavailable"
    body = getattr(exc, "body", None)
    error = body.get("error") if isinstance(body, dict) else None
    code = error.get("type") if isinstance(error, dict) else None
    known = {"CAPACITY_LIMIT", "USER_CONCURRENCY_LIMIT", "CONCURRENCY_REQUEST_LIMIT", "budget_exceeded"}
    return code if code in known else "RATE_LIMITED" if exc.status == 429 else "unavailable"


async def decide(state: dict, questions: dict):
    # Serial calls respect the universal-key concurrency ceiling. Queue time is bounded too.
    async with asyncio.timeout(7):
        async with _serial:
            return await get_jev_client().system_one(
                model=os.environ["JEV_MODEL"], state=state, questions=questions)


async def close_jev():
    if get_jev_client.cache_info().currsize:
        await get_jev_client().aclose()
        get_jev_client.cache_clear()