from django.urls import path
from .views import UserListView, UserUpdateView

urlpatterns = [
    path('users/', UserListView.as_view(), name="users"),
    path('users/<int:pk>/change', UserUpdateView.as_view(), name="change"),
]