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
    path('DriverDocketEntry/<int:ids>/', views.driverDocketEntry, name='driverDocketEntry'),      
    path('DriverDocketEntrySave/<int:ids>/', views.driverDocketEntrySave, name='driverDocketEntrySave'),      
    
    # Account Tables 
    # Base plant routes
    path('BasePlantTable/', views.basePlantTable, name='basePlantTable'),
    path('BasePlant/add/', views.basePlantForm, name='basePlantAdd'),
    path('BasePlant/add/save/', views.basePlantSave, name='basePlantAddSave'),   
    path('BasePlant/edit/<int:id>/', views.basePlantForm, name='basePlantEdit'),      
    path('BasePlant/edit/save/<int:id>/', views.basePlantSave, name='basePlantEditSave'),   

    path('RctiTable/', views.rctiTable, name='rctiTable'),
    path('DriverTripsTable/', views.driverTripsTable, name='driverTripsTable'),
    
    
    # DriverTrip Csv
    path('DriverTripCsv/', views.driverTripCsv, name='driverTripCsv'),  
    path('RctiCsvForm/', views.rctiCsvForm, name='rctiCsvForm'),  
    path('DriverSampleCsv/', views.driverSampleCsv, name='driverSampleCsv'),  
    
    # Edit
    path('driverTrip/edit/<int:id>/', views.DriverTripEditForm, name='DriverTripEdit'), 
    path('driverTrip/update/<int:ids>/', views.driverEntryUpdate, name='driverEntryUpdate'), 
    # path('natureOfLeaves/edit/save/<int:id>/', views.changeNatureOfLeaves, name='editSaveNatureOfLeaves'),
    
    # Filters
    path('verifiedFilter/', views.verifiedFilter, name='verifiedFilter'),  
    path('clientFilter/', views.clientFilter, name='clientFilter'),  
    path('dateRangeFilter/', views.dateRangeFilter, name='dateRangeFilter'),


    # Reconciliation
    path('reconciliation/form/', views.reconciliationForm, name='reconciliationForm'),
    path('reconciliation/analysis/', views.reconciliationAnalysis, name='reconciliationAnalysis'),
    path('reconciliation/result/', views.reconciliationResult, name='reconciliationResult'),
    path('reconciliation/docket/view/', views.reconciliationDocketView, name='reconciliationDocketView'),

    # Public holiday
    path('publicHoliday/', views.publicHoliday, name='publicHoliday'),
    path('publicHoliday/add/', views.publicHolidayForm, name='publicHolidayAdd'),
    path('publicHoliday/add/save/', views.publicHolidaySave, name='publicHolidaySave'),

    path('publicHoliday/edit/<int:id>/', views.publicHolidayForm, name='publicHolidayEdit'),
    path('publicHoliday/edit/save/<int:id>/', views.publicHolidaySave, name='publicHolidayEditSave'),

]
