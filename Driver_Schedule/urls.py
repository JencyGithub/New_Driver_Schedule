"""
URL configuration for Driver_Schedule project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path , include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # main index page
    path('', views.index, name='index'),
    path('login',views.loginCall, name='login'),
    path('loginCheck',views.loginCheck, name='login-check'),
    path('logout',views.CustomLogOut, name='logout'),

    # Account routes
    path('account/',include('Account_app.urls')),

    # GearBox routes
    path('gearBox/',include('GearBox_app.urls')),
    
]