from django.urls import path

from .views import create, delete, index, update

urlpatterns = [
    path('', index, name="statuses_list"),
    path('create/', create, name="create_status"),
    path('update/<int:status_id>', update, name="update_status"),
    path('delete/<int:status_id>', delete, name="delete_status"),
]
