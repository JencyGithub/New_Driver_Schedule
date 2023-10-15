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

app_name = 'Account'

urlpatterns = [
    path('', views.index, name='index'), 
    # Driver trip path
    path('Form1/', views.getForm1, name='getForm1'), 
    path('Form2/', views.getForm2, name='getForm2'),
    
     path('createFormSession/',
         views.createFormSession, name='createFormSession'),
    path('formsSave/', views.formsSave, name='formsSave'),

    path('getTrucks/', views.getTrucks, name='getTrucks'), 
    
    path('Rcti/', views.rcti, name='rcti'), 
    path('RctiSave/', views.rctiSave, name='rctiSave'), 
    path('DriverEntry/', views.driverEntry, name='driverentry'), 
    path('DriverEntrySave/', views.driverEntrySave, name='driverEntrySave'),      
    
    # Account Tables 
    path('BasePlantTable/', views.basePlantTable, name='basePlantTable'),      
    path('RctiTable/', views.rctiTable, name='rctiTable'),      
    path('DriverTripsTable/', views.driverTripsTable, name='driverTripsTable'),  
    
    # DriverTrip Csv
    path('DriverTripCsv/', views.driverTripCsv, name='driverTripCsv'),  
    
    # Edit
    path('driverTrip/edit/<int:id>/', views.DriverTripEditForm, name='DriverTripEdit'), 
    # path('natureOfLeaves/edit/save/<int:id>/', views.changeNatureOfLeaves, name='editSaveNatureOfLeaves'),
    
]
