from django.db import models

from config import settings
from users.models import AuditFields, AutoAuditMixin, SoftDeleteModel


class Goal(AutoAuditMixin, AuditFields, SoftDeleteModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="goals"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def delete(self):
        for t in self.todos.alive():
            t.delete()
        return super().delete()


class Todo(AutoAuditMixin, AuditFields, SoftDeleteModel):
    class Status(models.TextChoices):
        TODO = "TODO"
        IN_PROGRESS = "IN_PROGRESS"
        DONE = "DONE"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="todos"
    )
    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, related_name="todos", null=True, blank=True
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    memo = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.TODO
    )
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["owner", "due_date"]),
            models.Index(fields=["goal_id", "due_date"]),
        ]
