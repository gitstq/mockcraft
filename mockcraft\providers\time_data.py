"""
MockCraft Time Provider - datetime, date, timestamp.
"""
import random
from datetime import datetime, timedelta


class TimeProvider:
    """Generates time-related data."""

    # Common date/time formats
    FORMATS = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d",
        "%Y/%m/%d %H:%M:%S",
        "%d/%m/%Y",
        "%d/%m/%Y %H:%M:%S",
        "%Y%m%d",
        "%Y%m%d%H%M%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
    ]

    def generate(self, format: str = "%Y-%m-%d %H:%M:%S", offset_days: int = 0, offset_hours: int = 0, **kwargs) -> str:
        """
        Generate a datetime string.

        Args:
            format: strftime format string
            offset_days: offset from today in days (can be negative)
            offset_hours: offset from now in hours (can be negative)
        """
        now = datetime.now()
        if offset_days:
            now += timedelta(days=offset_days)
        if offset_hours:
            now += timedelta(hours=offset_hours)

        try:
            return now.strftime(format)
        except Exception:
            return now.strftime("%Y-%m-%d %H:%M:%S")

    def date_generate(self, format: str = "%Y-%m-%d", offset_days: int = 0, **kwargs) -> str:
        return self.generate(format=format, offset_days=offset_days)

    def datetime_generate(self, format: str = "%Y-%m-%d %H:%M:%S", offset_days: int = 0, **kwargs) -> str:
        return self.generate(format=format, offset_days=offset_days)

    def timestamp_generate(self, offset_seconds: int = 0, **kwargs) -> int:
        """Return Unix timestamp."""
        now = datetime.now()
        if offset_seconds:
            now += timedelta(seconds=offset_seconds)
        return int(now.timestamp())

    def iso8601(self, **kwargs) -> str:
        return self.generate(format="%Y-%m-%dT%H:%M:%SZ", **kwargs)
