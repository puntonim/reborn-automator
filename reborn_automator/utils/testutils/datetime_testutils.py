from contextlib import ContextDecorator
from datetime import datetime, timezone
from unittest import mock


class freeze_time(ContextDecorator):
    """
    Context manager and decorator to simulate that today is the given date, but limited
     to `utils.datetime_utils` module.

    As a context manager:
        sunday_night = datetime(2022, 1, 23, 22, 15, 0).astimezone()
        with datetime_testutils.freeze_time(sunday_night)
            assert datetime_utils.now() == sunday_night

    As decorator, you can decorate a test function or method like:
        sunday_night = datetime(2022, 1, 23, 22, 15, 0).astimezone()
        @datetime_testutils.freeze_time(sunday_night)
        def test_happy_flow(...):
            assert datetime_utils.now() == sunday_night

    But you can NOT decorate a (test) class. To use it for the entire test class:
        class TestMyTest:
            def setup(self):
                self.freeze_time = datetime_testutils.freeze_time(sunday_night)
                self.freeze_time.__enter__()

            def teardown(self):
                self.freeze_time.__exit__()
    """

    def __init__(self, date: datetime):
        self.date = date
        self.mock0 = None
        self.mock1 = None

    def __enter__(self):
        self.mock0 = mock.patch(
            "patatrack_utils.datetime_utils.now_utc",
            return_value=self.date.astimezone(timezone.utc),
        )
        self.mock0.start()

        self.mock1 = mock.patch(
            "patatrack_utils.datetime_utils.now",
            return_value=self.date.astimezone(),
        )
        self.mock1.start()

    def __exit__(self, *exc):
        self.mock0.stop()
        self.mock1.stop()


class approx_now:
    """
    Use it in tests to compare against now (the real now, it avoids getting the
     mocked now).

    Example:
        now = datetime(2023, 12, 8, 9, 33)

        @datetime_testutils.freeze_time(now)
        def test_happy_flow(self):
            ...
            assert pending_trade_models[0].to_dict() == {
                        "id": 1,
                        "created_at": datetime(2023, 12, 8, 8, 33, tzinfo=timezone.utc),
                        "updated_at": approx_now(buffer_seconds=10),
                        "trade_action": "SOLD",
                        ...
                    }
    """

    def __init__(self, buffer_seconds: int = 60):
        self.buffer_seconds = buffer_seconds

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                other = datetime.fromisoformat(other)
            except Exception as exc:
                pass
        if not isinstance(other, datetime):
            raise TypeError(f"Not a datetime: {other}")

        other = other.astimezone(tz=timezone.utc)
        now = datetime.now(tz=timezone.utc)

        if abs((other - now).total_seconds()) <= self.buffer_seconds:
            return True
        return False
