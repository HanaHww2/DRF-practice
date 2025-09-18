from django.contrib.auth.models import AbstractUser
from django.db import models

from commerce.mangers import AllUserManager, UserManager
from common.models import AutoAuditModel, SoftDeleteModel


class User(SoftDeleteModel, AutoAuditModel, AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False)

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


class Product(SoftDeleteModel, AutoAuditModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Order(SoftDeleteModel, AutoAuditModel):
    class Status(models.TextChoices):
        PENDING = "pending"
        CONFIRMED = "confirmed"
        DELIVERED = "delivered"
        CANCELLED = "cancelled"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=500)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    products = models.ManyToManyField(
        Product, through="OrderItem", related_name="orders"
    )

    def __str__(self):
        return f"Order {self.order_id } by {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"
