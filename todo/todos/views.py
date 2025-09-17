from collections import defaultdict
from django.utils.dateparse import parse_date
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from todos.models import Goal, Todo
from todos.serializers import GoalSerializer, TodoSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "owner"):
            return obj.owner == request.user

        if hasattr(obj, "goal") and obj.goal:
            return obj.goal.owner == request.user
        return False


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    ordering = ["-created_at"]

    def get_queryset(self):
        u = self.request.user
        qs = Todo.objects.alive().filter(owner=u)

        date_str = self.request.query_params.get("date")
        start_str = self.request.query_params.get("start")
        end_str = self.request.query_params.get("end")

        if date_str:
            d = parse_date(date_str)
            if d:
                qs = qs.filter(due_date=d)
        elif start_str and end_str:
            s, e = parse_date(start_str), parse_date(end_str)
            if s and e:
                qs = qs.filter(due_date__range=[s, e])

        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)

        goal_id = self.request.query_params.get("goalId")
        if goal_id:
            qs = qs.filter(goal_id=goal_id)

        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"], url_path="group-by-day")
    def group_by_day(self, request):
        qs = self.get_queryset().exclude(due_date__isnull=True)
        grouped = defaultdict(list)

        for t in qs:
            grouped[str(t.due_date)].append(
                TodoSerializer(t, context={"request": request}).data
            )
        return Response(grouped)


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Goal.objects.alive().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response(status=stauts.HTTP_204_NO_CONTENT)
