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
from GearBox_app import views

app_name = 'gearBox'

urlpatterns = [
    path('leaveReq/', views.leaveReq, name='leaveReq'), 
    path('natureOfLeaves/', views.natureOfLeaves, name='natureOfLeaves'), 
    
    # CRUD Nature of leaves
    path('natureOfLeaves/add/', views.addNatureOfLeave, name='addNatureOfLeave'), 
    path('natureOfLeaves/edit/', views.natureOfLeavesEdit, name='natureOfLeavesEdit'), 


    # CRUD Leave Request
    # ADD
    path('leaveReqForm/', views.leaveReqForm, name='leaveReqForm'), 
    path('leaveRequest/add/', views.changeLeaveRequest, name='addLeaveRequest'), 
    # UPDATE
    path('leaveReq/edit/<int:id>/', views.leaveReqForm, name='leaveReqEdit'), 
    path('leaveRequest/edit/save/<int:id>/', views.changeLeaveRequest, name='editSaveLeaveRequest'), 
]