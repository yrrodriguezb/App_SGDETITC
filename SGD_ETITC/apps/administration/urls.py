from django.urls import path
from .views import UserListView, getUserById, update_user, delete_user

urlpatterns = [
    path('users/', UserListView.as_view(), name="users"),
    path('user/<str:pk>/', getUserById, name="get_user"),
    path('user/<str:pk>/change/', update_user, name="update_user"),
    path('user/<str:pk>/delete/', delete_user, name="delete_user"),
]