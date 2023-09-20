from django.urls import path

from .views import (TasksCreateView, TasksDeleteView, TasksListView,
                    TasksUpdateView)

urlpatterns = [
    path('', TasksListView.as_view(), name="tasks_list"),
    path('create/', TasksCreateView.as_view(), name="create_task"),
    path('update/<int:pk>', TasksUpdateView.as_view(), name="update_task"),
    path('delete/<int:pk>', TasksDeleteView.as_view(), name="delete_task"),
]
