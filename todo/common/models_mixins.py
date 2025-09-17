from django.db import models

from common.middleware import get_current_user


class AutoAuditMixin(models.Model):
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
