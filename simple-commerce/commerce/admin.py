from django.contrib import admin

from commerce.models import OrderItem, Order, User, Product


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(User)
