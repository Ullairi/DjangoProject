from django.core.serializers import serialize
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from test_app.models import Task
from test_app.serializers.task import TaskSerializer
from django.utils import timezone
from django.db.models import Count


class TaskView(APIView):
    def post(self, request):
        task_dto = TaskSerializer(data=request.data)
        if task_dto.is_valid():
            task_dto.save()
            return Response(task_dto.data, status=status.HTTP_201_CREATED)
        return Response(task_dto.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskListView(APIView):
    def get(self, request):
        queryset = Task.objects.all()
        task_dto = TaskSerializer(queryset, many=True)
        return Response(task_dto.data)

class TaskIdView(APIView):
    def get(self, request, task_id):
        try:
            queryset = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)
        task_dto = TaskSerializer(queryset)
        return Response(task_dto.data)


class TaskStatsView(APIView):
    def get(self, request):
        amount = Task.objects.count()
        stats = Task.objects.values("status").annotate(count=Count("status"))
        overdue = Task.objects.filter(deadline__lt=timezone.now()).count()

        return Response({
            "total_tasks": amount,
            "tasks_by_status": stats,
            "overdue_tasks": overdue
        })



def home_page(request, user_name):
    return HttpResponse(f"Hello, {user_name}")