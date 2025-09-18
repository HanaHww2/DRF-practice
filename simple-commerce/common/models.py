from datetime import timezone
from django.db import models

from common.middleware import get_current_user


class AutoAuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.BigIntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and user.is_authenticated:
            uid = user.pk
            if not self.pk and hasattr(self, "created_by") and self.created_by is None:
                self.created_by = uid
            if hasattr(self, "updated_by"):
                self.updated_by = uid
        return super().save(*args, **kwargs)


class SoftDeleteQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.filter(deleted_at__isnull=False)

    def delete(self):
        updates = {"deleted_at": timezone.now()}
        try:
            self.model._meta.get_field("deleted_by")
            user = get_current_user()
            uid = user.pk if user and user.is_authenticated else None
            updates["deleted_by"] = uid
        except:
            pass
        return super().update(**updates)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.BigIntegerField(null=True, blank=True)

    objects = SoftDeleteQuerySet().as_manager()

    class Meta:
        abstract = True

    def delete(self):
        if self.deleted_at:
            return

        user = get_current_user()
        uid = user.pk if user and user.is_authenticated else None

        if uid:
            self.deleted_by = uid
        self.deleted_at = timezone.now()

        self.save(update_fields=["deleted_at", "deleted_by"])

    def hard_delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def restore(self):
        if self.deleted_at is None:
            return
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])
