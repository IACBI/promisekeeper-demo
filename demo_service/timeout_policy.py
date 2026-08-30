"""Small retry boundary used to demonstrate outcome-specific GitHub evidence."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar


ResultT = TypeVar("ResultT")


class RetryTimeoutError(TimeoutError):
    """Raised after the configured timeout attempts are exhausted."""


@dataclass(frozen=True)
class RetryPolicy:
    timeout_seconds: float
    max_attempts: int

    def __post_init__(self) -> None:
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least one")


def execute_with_retry(
    operation: Callable[[float], ResultT],
    policy: RetryPolicy,
) -> ResultT:
    """Retry timeouts within an explicit bound and preserve the final cause."""

    for attempt in range(1, policy.max_attempts + 1):
        try:
            return operation(policy.timeout_seconds)
        except TimeoutError as error:
            if attempt == policy.max_attempts:
                raise RetryTimeoutError(
                    f"operation timed out after {policy.max_attempts} attempts"
                ) from error

    raise AssertionError("retry loop must return or raise")
