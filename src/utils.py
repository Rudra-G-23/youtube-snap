class TimeConverter:
    """Utility class for Time Conversion."""

    _MILLISECONDS_PER_SECONDS: int = 1_000
    _SECONDS_PER_MINUTE: int = 60
    _MINUTES_PER_HOUR: int = 60

    @classmethod
    def to_milliseconds(cls, *, hour: int, minute: int, second: int) -> int:
        """Convert hour, minute, second into milliseconds."""

        if hour < 0 or minute < 0 or second < 0:
            raise ValueError("Time is not correct!")

        total_seconds = (
            hour * cls._MINUTES_PER_HOUR * cls._SECONDS_PER_MINUTE
            + minute * cls._SECONDS_PER_MINUTE
            + second
        )

        total_milliseconds = total_seconds * cls._MILLISECONDS_PER_SECONDS

        return total_milliseconds


if __name__ == "__main__":
    print("\nMilliseconds:", TimeConverter.to_milliseconds(hour=1, minute=24, second=45))
