from django.urls import path

from .views import create, delete, index, login_user, update, logout_user

urlpatterns = [
    path('', index, name="users_list"),
    path('login/', login_user, name="login_user"),
    path('logout/', logout_user, name="logout_user"),
    path('create/', create, name="create_user"),
    path('<int:user_id>/update', update, name="update_user"),
    path('<int:user_id>/delete', delete, name="delete_user"),
]
