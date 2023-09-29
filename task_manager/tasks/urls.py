from django.urls import path

from .views import (TasksCreateView, TasksDeleteView, TasksListView,
                    TasksUpdateView, TaskDetailView)

urlpatterns = [
    path('', TasksListView.as_view(), name="tasks_list"),
    path('<int:pk>/', TaskDetailView.as_view(), name="detail_task"),
    path('create/', TasksCreateView.as_view(), name="create_task"),
    path('<int:pk>/update/', TasksUpdateView.as_view(), name="update_task"),
    path('<int:pk>/delete/', TasksDeleteView.as_view(), name="delete_task"),
]
