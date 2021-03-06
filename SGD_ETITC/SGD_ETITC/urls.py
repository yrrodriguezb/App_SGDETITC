"""SGD_ETITC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from apps.authentication.views import (
    LoginView, 
    LogoutView, 
    PasswdChangeView, 
    PasswdResetView,
    PasswdResetConfirmView,
    PasswdResetDoneView,
    UserCreateView
)

admin.site.login = login_required(admin.site.login)
admin.site.site_header = "SGD ETITC - Admin"
admin.site.site_title = "SGD ETITC - Portal"
admin.site.index_title = "Bienvenido al Portal SGD ETITC"

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('administration/', include('apps.administration.urls')),
    path('core/', include('apps.core.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswdChangeView.as_view(), name='password_change'),
    path('password_reset/', PasswdResetView.as_view(), name='password_reset'),
    path('password_reset/<uidb64>/<token>/',PasswdResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/done/', PasswdResetDoneView.as_view(), name='password_reset_complete'),
    path('profile/', include('apps.profile.urls')),
    path('register_me', UserCreateView.as_view(), name='register_me'),   
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
