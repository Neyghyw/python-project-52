from django.urls import path

from .views import create, delete, index, update

urlpatterns = [
    path('', index, name="labels_list"),
    path('create/', create, name="create_label"),
    path('update/<int:label_id>', update, name="update_label"),
    path('delete/<int:label_id>', delete, name="delete_label"),
]
