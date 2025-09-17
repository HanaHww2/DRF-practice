from django.contrib import admin

from todos.models import Goal, Todo

# Register your models here.
admin.site.register(Todo)
admin.site.register(Goal)
