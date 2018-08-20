from django.urls import path
from .views import ProfileView, update_profile

urlpatterns = [
    path('', ProfileView.as_view(), name="profile"),
    path('change/<int:pk>/', update_profile, name="change_profile"),
]