from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from commerce.models import Order
from commerce.serializers import OrderSerializer, ProductSerializer, UserSerializer
from common.permissions import IsSelfOrAdmin, IsUsersOrAdmin


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.alive().prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()

        if self.action == "list" and not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    def get_permissions(self):
        method = self.request.method

        if method in ["GET", "PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAuthenticated, IsUsersOrAdmin]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        method = self.request.method

        if method == "POST":
            self.permission_classes = [AllowAny]
        elif method == "GET" and not self.kwargs.get("pk"):
            self.permission_classes = [IsAdminUser]
        elif method == "GET":
            self.permission_classes = [IsAuthenticated, IsSelfOrAdmin]
        elif method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAuthenticated, IsSelfOrAdmin]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()
