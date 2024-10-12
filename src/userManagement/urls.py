"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from userManagement.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', LoginView.as_view(template_name='userManagement/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('information', user_info_view, name='user_info'),
    path('noaccess', no_access_view, name='access_denied'),
    path('init', init_view, name='init'),
    path('get_notifications', get_notifications, name='get_notifications'),
    path('send', some_event_trigger, name='some_event_trigger'),
    path('notify_driver_sms', notify_driver_sms, name='notify_driver_sms'),
    path('mynotification/<str:notification_id>', load_my_notification, name='load_my_notification'),
]
