from django.urls import path
from . import views

urlpatterns = [
    path('api/get-task-list/', views.GetTaskList.as_view(), name='get_task_list'),
    path('api/create-task/', views.CreateTask.as_view(), name='create_task'),
    path('api/update-task/', views.UpdateTask.as_view(), name='update_task'),
    path('api/delete-task/', views.DeleteTask.as_view(), name='delete_task'),
]
