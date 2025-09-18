from dataclasses import field, fields
from django.db import transaction
from rest_framework import serializers

from commerce.models import Order, OrderItem, Product, User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "price", "stock")
        read_only_fields = ("id",)

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="product.price", read_only=True
    )

    class Meta:
        model = OrderItem
        fields = (
            "product",
            "product_name",
            "product_price",
            "quantity",
            "item_subtotal",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    total_price = serializers.SerializerMethodField(method_name="total", read_only=True)

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    def update(self, instance, validated_data):
        orderitem_data = None
        if "items" in validated_data:
            orderitem_data = validated_data.pop("items")

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if orderitem_data is not None:
                instance.items.all().delete()

                for item in orderitem_data:
                    OrderItem.objects.create(order=instance, **item)
        return instance

    def create(self, validated_data):
        orderitem_data = None
        if "items" in validated_data:
            orderitem_data = validated_data.pop("items")

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item in orderitem_data:
                OrderItem.objects.create(order=order, **item)

        return order

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "status",
            "items",
            "total_price",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at", "user")


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "email", "password"]

    def create(self, validated_data):
        with transaction.atomic():
            user = User(email=validated_data["email"])
            user.set_password(validated_data["password"])
            user.save()
            return user
