from django.urls import path

from .views import create, delete, index, update

urlpatterns = [
    path('', index, name="tasks_list"),
    path('create/', create, name="create_task"),
    path('update/<int:pk>', update, name="update_task"),
    path('delete/<int:pk>', delete, name="delete_task"),
]
