"""Business-day deadline rules for the controlled F1 flow."""

from dataclasses import dataclass
from datetime import date, timedelta

from mira.domain.policy import ControlledCase


MONTHS_ES = (
    "ene",
    "feb",
    "mar",
    "abr",
    "may",
    "jun",
    "jul",
    "ago",
    "sep",
    "oct",
    "nov",
    "dic",
)


@dataclass(frozen=True)
class CaseDeadlines:
    internal_due: date
    contractual_due: date
    internal_label: str
    contractual_label: str
    internal_state: str
    contractual_state: str
    supervisor_mark: bool

    @property
    def summary(self) -> str:
        if self.contractual_state == "Vencido":
            return "Plazo contractual vencido"
        if self.contractual_state == "Alerta previa":
            return "Alerta previa contractual"
        if self.internal_state == "Vencido":
            return "Plazo interno vencido"
        if self.internal_state == "Alerta previa":
            return "Alerta previa interna"
        if self.internal_state == "Vence hoy" or self.contractual_state == "Vence hoy":
            return "Vence hoy"
        return "Vigente"


def is_business_day(day: date) -> bool:
    return day.weekday() < 5


def add_business_days(start: date, days: int) -> date:
    current = start
    remaining = days
    while remaining:
        current += timedelta(days=1)
        if is_business_day(current):
            remaining -= 1
    return current


def previous_business_day(day: date) -> date:
    current = day
    while True:
        current -= timedelta(days=1)
        if is_business_day(current):
            return current


def classify_deadline(today: date, due: date) -> str:
    if today > due:
        return "Vencido"
    if today == due:
        return "Vence hoy"
    if today == previous_business_day(due):
        return "Alerta previa"
    return "Vigente"


def format_deadline(day: date) -> str:
    return f"{day.day:02d} {MONTHS_ES[day.month - 1]} {day.year}"


def evaluate_deadlines(case: ControlledCase, today: date) -> CaseDeadlines:
    internal_due = add_business_days(case.received_date, 3)
    contractual_due = add_business_days(case.received_date, 5)
    contractual_state = classify_deadline(today, contractual_due)
    return CaseDeadlines(
        internal_due=internal_due,
        contractual_due=contractual_due,
        internal_label=format_deadline(internal_due),
        contractual_label=format_deadline(contractual_due),
        internal_state=classify_deadline(today, internal_due),
        contractual_state=contractual_state,
        supervisor_mark=contractual_state == "Vencido",
    )
