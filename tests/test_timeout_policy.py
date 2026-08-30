import unittest

from demo_service.timeout_policy import RetryPolicy, RetryTimeoutError, execute_with_retry


class TimeoutPolicyTest(unittest.TestCase):
    def test_retries_with_the_configured_timeout_before_succeeding(self) -> None:
        observed_timeouts: list[float] = []

        def operation(timeout_seconds: float) -> str:
            observed_timeouts.append(timeout_seconds)
            if len(observed_timeouts) == 1:
                raise TimeoutError("first attempt timed out")
            return "completed"

        result = execute_with_retry(
            operation,
            RetryPolicy(timeout_seconds=2.5, max_attempts=2),
        )

        self.assertEqual(result, "completed")
        self.assertEqual(observed_timeouts, [2.5, 2.5])

    def test_raises_after_the_bounded_number_of_timeouts(self) -> None:
        def operation(_: float) -> str:
            raise TimeoutError("still unavailable")

        with self.assertRaisesRegex(RetryTimeoutError, "after 2 attempts"):
            execute_with_retry(
                operation,
                RetryPolicy(timeout_seconds=1.0, max_attempts=2),
            )


if __name__ == "__main__":
    unittest.main()
