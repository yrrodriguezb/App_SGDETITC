from django.urls import path
from .views import HomePageView, send_email

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('send_mail/', send_email, name="email")
]