from django.core.serializers import serialize
from django.http import HttpResponse
from django.template.context_processors import request
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from test_app.models import Task, SubTask
from test_app.serializers.task import TaskCreateSerializer, TaskDetailSerializer, TaskSerializer
from test_app.serializers.subtask import SubTaskCreateSerializer
from django.utils import timezone
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination


@api_view(['POST'])
def create_task(request):
    task_dto = TaskCreateSerializer(data=request.data)
    if task_dto.is_valid():
        task_dto.save()
        return Response(task_dto.data, status=status.HTTP_201_CREATED)
    return Response(task_dto.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_task(request):
    queryset = Task.objects.all()
    task_dto = TaskSerializer(queryset, many=True)
    return Response(task_dto.data)

@api_view(['GET'])
def id_task(request, task_id):
    try:
        queryset = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)
    task_dto = TaskDetailSerializer(queryset)
    return Response(task_dto.data)


@api_view(['GET'])
def stats_task(request):
    amount = Task.objects.count()
    stats = Task.objects.values("status").annotate(count=Count("status"))
    overdue = Task.objects.filter(deadline__lt=timezone.now()).count()

    return Response({
        "total_tasks": amount,
        "tasks_by_status": stats,
        "overdue_tasks": overdue
    })

class SubTaskListCreateView(APIView):
    def get(self, request):
        queryset = SubTask.objects.all().order_by("-created_at")

        paginator = SubTaskPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = SubTaskCreateSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        subtask_dto = SubTaskCreateSerializer(data=request.data)
        if subtask_dto.is_valid():
            subtask_dto.save()
            return Response(subtask_dto.data, status=status.HTTP_201_CREATED)
        return Response(subtask_dto.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get_id(self, subtask_id):
        try:
            return SubTask.objects.get(id=subtask_id)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, subtask_id):
        object = self.get_id(subtask_id)
        if object is None:
            return Response({"error": "Subtask was not found"}, status=404)

        subtask_dto = SubTaskCreateSerializer(object)
        return Response(subtask_dto.data)

    def put(self, request, subtask_id):
        object = self.get_id(subtask_id)
        if object is None:
            return Response({"error": "Subtask was not found"}, status=404)

        subtask_dto = SubTaskCreateSerializer(object, data=request.data)
        if subtask_dto.is_valid():
            subtask_dto.save()
            return Response(subtask_dto.data)
        return Response(subtask_dto.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subtask_id):
        object = self.get_id(subtask_id)
        if object is None:
            return Response({"error": "SubTask not found"}, status=404)

        object.delete()
        return Response(status=204)

class GetTaskList(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all().order_by("-created_at")
        day_of_week = self.request.query_params.get("day_of_week", None)

        if day_of_week:
            days = {
                'monday': 2,
                'tuesday': 3,
                'wednesday': 4,
                'thursday': 5,
                'friday': 6,
                'saturday': 7,
                'sunday': 1,
                'понедельник': 2,
                'вторник': 3,
                'среда': 4,
                'четверг': 5,
                'пятница': 6,
                'суббота': 7,
                'воскресенье': 1,
            }
            day_number = days.get(day_of_week.lower())
            if day_number:
                queryset = queryset.filter(deadline__week_day=day_number)
        return queryset

class SubTaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class SubTaskFilter(GenericAPIView):
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination

    def get_queryset(self):
        queryset = SubTask.objects.all().order_by("-created_at")

        task_title = self.request.query_params.get("task_title")
        status_filter = self.request.query_params.get("status")

        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title.strip())

        if status_filter:
            queryset = queryset.filter(status__iexact=status_filter.strip())

        return queryset

    def get(self,request):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




def home_page(request, user_name):
    return HttpResponse(f"Hello, {user_name}")

