from typing import Protocol


class ReviewRepository(Protocol):
    def save(
        self, case_id: str, expected_case_version: int, kind: str, payload: dict
    ): ...


class Clock(Protocol):
    def now(self): ...
    def today(self): ...
