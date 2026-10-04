from datetime import datetime
from zoneinfo import ZoneInfo


class ControlledClock:
    def __init__(self, instant=None):
        self.instant = instant or datetime(
            2026, 10, 6, 12, tzinfo=ZoneInfo("America/Santiago")
        )

    def now(self):
        return self.instant.astimezone(ZoneInfo("America/Santiago"))

    def today(self):
        return self.now().date()


clock = ControlledClock()
