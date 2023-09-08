from django.urls import path

from .views import (UserCreateView, UserDeleteView, UserListView,
                    UserLoginView, UserLogoutView, UserUpdateView)

urlpatterns = [
    path('', UserListView.as_view(), name="users_list"),
    path('login/', UserLoginView.as_view(), name="login_user"),
    path('logout/', UserLogoutView.as_view(), name="logout_user"),
    path('create/', UserCreateView.as_view(), name="create_user"),
    path('<int:pk>/update', UserUpdateView.as_view(), name="update_user"),
    path('<int:pk>/delete', UserDeleteView.as_view(), name="delete_user"),
]
