from django.core.management.base import BaseCommand
from mira.infrastructure.controlled_cases import demo_cases
from mira.infrastructure.review_store import seed_case


class Command(BaseCommand):
    help = "Carga idempotente del corpus ficticio F4/F1; conserva intervenciones."

    def handle(self, *args, **options):
        for case in demo_cases():
            seed_case(case)
        self.stdout.write(
            self.style.SUCCESS("15 Casos ficticios disponibles; historial conservado.")
        )
