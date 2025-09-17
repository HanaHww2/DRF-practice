from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import AuditFields, SoftDeleteModel
from common.models_mixins import AutoAuditMixin
from .managers import AllUserManager, UserManager


class User(AutoAuditMixin, AuditFields, SoftDeleteModel, AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)

    objects = UserManager()
    all_objects = AllUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or f"user:{self.pk}"

    def delete(self):
        if self.deleted_at:
            return

        self.is_active = False
        self.email = None
        self.first_name = None
        self.last_name = None

        return super().delete()
