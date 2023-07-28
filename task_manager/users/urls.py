from django.urls import path

from .views import create, delete, index, login_user, update

urlpatterns = [
    path('', index, name="users_list"),
    path('login/', login_user, name="login_user"),
    path('create/', create, name="create_user"),
    path('update/', update, name="update_user"),
    path('delete/', delete, name="delete_user"),
]
