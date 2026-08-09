import json
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Task



def get_task_list_data_fun(data):
    try:
        status = data.get("status")

        tasks_queryset = Task.objects.all()

        if status:
            tasks_queryset = tasks_queryset.filter(status=status)

        tasks_data = list(
            tasks_queryset.values(
                "id",
                "title",
                "description",
                "priority",
                "status",
                "due_date",
                "created_at",
                "updated_at",
            )
        )

        return JsonResponse({
            "status": "success",
            "message": "Tasks fetched successfully",
            "payload": {"tasks": tasks_data}
        })

    except Exception as e:
        return JsonResponse({"message": str(e), "status": "error", "remarks": "Unknown Error", "payload": {}}, status=500)


class GetTaskList(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            return get_task_list_data_fun(data)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON", "status": "error", "remarks": "JSON Error", "payload": {}}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e), "status": "error", "remarks": "Unknown Error", "payload": {}}, status=500)




def create_task_data_fun(data):
    try:
        title = (data.get("title") or "").strip()

        if not title:
            return JsonResponse({"status": "error", "message": "title is required", "remarks": "Validation Error", "payload": {}}, status=400)

        task = Task.objects.create(
            title=title,
            description=data.get("description"),
            priority=data.get("priority", "medium"),
            status=data.get("status", "pending"),
            due_date=data.get("due_date"),
        )

        return JsonResponse({
            "status": "success",
            "message": "Task created successfully",
            "payload": {
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority,
                    "status": task.status,
                    "due_date": task.due_date,
                }
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({"message": str(e), "status": "error", "remarks": "Unknown Error", "payload": {}}, status=500)


class CreateTask(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            return create_task_data_fun(data)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON", "status": "error", "remarks": "JSON Error", "payload": {}}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e), "status": "error", "remarks": "Unknown Error", "payload": {}}, status=500)




def update_task_data_fun(data):
    try:
        task_id = data.get("taskId")

        if not task_id:
            return JsonResponse({"status": "error", "message": "taskId is required", "remarks": "Validation Error", "payload": {}}, status=400)

        task = Task.objects.filter(id=task_id).first()

        if not task:
            return JsonResponse({"status": "error", "message": "Task not found", "remarks": "Not Found", "payload": {}}, status=404)

        for field in ["title", "description", "priority", "status", "due_date"]:
            if field in data:
                setattr(task, field, data[field])

        task.save()

        return JsonResponse({
            "status": "success",
            "message": "Task updated successfully",
            "payload": {
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority,
                    "status": task.status,
                    "due_date": task.due_date,
                }
            }
        })

    except Exception as e:
        return JsonResponse({"message": str(e), "status": "error", "remarks": "Unknown Error", "payload": {}}, status=500)


class UpdateTask(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            return update_task_data_fun(data)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON", "status": "error", "remarks": "JSON Error", "payload": {}}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e), "status": "error", "remarks": "Unknown Error", "payload": {}}, status=500)




def delete_task_data_fun(data):
    try:
        task_id = data.get("taskId")

        if not task_id:
            return JsonResponse({"status": "error", "message": "taskId is required", "remarks": "Validation Error", "payload": {}}, status=400)

        task = Task.objects.filter(id=task_id).first()

        if not task:
            return JsonResponse({"status": "error", "message": "Task not found", "remarks": "Not Found", "payload": {}}, status=404)

        task.delete()

        return JsonResponse({
            "status": "success",
            "message": "Task deleted successfully",
            "payload": {}
        })

    except Exception as e:
        return JsonResponse({"message": str(e), "status": "error", "remarks": "Unknown Error", "payload": {}}, status=500)


class DeleteTask(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            return delete_task_data_fun(data)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON", "status": "error", "remarks": "JSON Error", "payload": {}}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e), "status": "error", "remarks": "Unknown Error", "payload": {}}, status=500)
