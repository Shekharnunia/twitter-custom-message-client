from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from twitter import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.list_message),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html')),
]
