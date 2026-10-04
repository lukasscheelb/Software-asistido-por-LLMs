from django.db import models


class CaseRecord(models.Model):
    case_id = models.CharField(max_length=80, primary_key=True)
    version = models.PositiveIntegerField(default=1)
    payload = models.JSONField()
    current_values = models.JSONField(default=dict)


class AppendOnlyQuerySet(models.QuerySet):
    def update(self, **kwargs):
        raise ValueError("El historial es append-only.")

    def delete(self):
        raise ValueError("El historial es append-only.")


class AppendOnlyRecord(models.Model):
    objects = AppendOnlyQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValueError("El historial es append-only.")
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("El historial es append-only.")


class EvaluationRecord(AppendOnlyRecord):
    case = models.OneToOneField(CaseRecord, on_delete=models.PROTECT)
    case_version = models.PositiveIntegerField(default=1)
    inputs = models.JSONField()
    policy = models.JSONField()
    result = models.JSONField()


class InterventionRecord(AppendOnlyRecord):
    case = models.ForeignKey(CaseRecord, on_delete=models.PROTECT)
    version = models.PositiveIntegerField()
    kind = models.CharField(max_length=20)
    payload = models.JSONField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["case", "version"], name="unique_case_intervention_version"
            )
        ]
        ordering = ["version"]
