from django.contrib.auth.base_user import BaseUserManager

from common.models import SoftDeleteModel, SoftDeleteQuerySet


SoftDeleteUserBase = BaseUserManager.from_queryset(SoftDeleteQuerySet)


class UserManager(SoftDeleteUserBase):
    use_in_migrations = True

    def get_queryset(self):
        return super().get_queryset().alive()

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("The Email must be set")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class AllUserManager(BaseUserManager):
    use_in_migrations = True
