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
    
    path('createFormSession/',views.createFormSession, name='createFormSession'),
    path('formsSave/', views.formsSave, name='formsSave'),

    path('getTrucks/', views.getTrucks, name='getTrucks'), 
    
    path('Rcti/', views.rcti, name='rcti'), 
    path('Rcti/Error/Solve/<int:id>', views.rctiErrorSolve, name='rctiErrorSolve'), 
    # Add RCTI manually
    path('rctiForm/', views.rctiForm, name='rctiFormAdd'), 
    path('rctiForm/save/', views.rctiFormSave, name='rctiFormSave'), 
    path('rctiForm/<int:id>/', views.rctiForm, name='rctiForm'), 
    path('RctiSave/', views.rctiSave, name='rctiSave'), 
    path('uploded/rcti/', views.uplodedRCTI, name='UplodedRCTI'), 
    path('rcti/error/get/', views.getRctiError, name='getRctiError'), 
    
    
    # Expanse entry manually
    path('expanse/', views.expanseForm, name='expanseForm'), 
    path('expanse/save/', views.expanseSave, name='expanseFormSave'), 
    path('expanse/<int:id>', views.expanseForm, name='expanseView'),  
    
    
    
    path('DriverEntry/', views.driverEntry, name='driverentry'), 
    path('DriverEntrySave/', views.driverEntrySave, name='driverEntrySave'),           
    path('DriverDocketEntry/<int:ids>/', views.driverDocketEntry, name='driverDocketEntry'),
    
    path('driverDocket/waitingTime/count/', views.countDocketWaitingTime, name='countDocketWaitingTime'),
    path('driverDocket/standByTime/count/', views.countDocketStandByTime, name='countDocketStandByTime'),

    
    path('DriverDocketEntrySave/<int:ids>/', views.driverDocketEntrySave, name='driverDocketEntrySave'), 
    # for error solve      
    path('DriverDocketEntrySave/<int:ids>/<int:errorId>', views.driverDocketEntrySave, name='driverDocketErrorEntrySave'),      
    
    # Account Tables 
    # Base plant routes
    path('BasePlantTable/', views.basePlantTable, name='basePlantTable'),
    path('BasePlant/add/', views.basePlantForm, name='basePlantAdd'),
    path('BasePlant/add/save/', views.basePlantSave, name='basePlantAddSave'),   
    path('BasePlant/edit/<int:id>/', views.basePlantForm, name='basePlantEdit'),      
    path('BasePlant/edit/save/<int:id>/', views.basePlantSave, name='basePlantEditSave'),   

    # Location
    path('location/save/', views.locationSave, name='locationSave'), 
    path('location/edit/<int:id>/', views.locationEditForm, name='locationEdit'),   
    path('location/edit/save/<int:id>', views.locationSave, name='locationEditSave'),   

    path('RctiTable/', views.rctiTable, name='rctiTable'),
    # path('DriverTripsTable/', views.driverTripsTable, name='driverTripsTable'),

    # Rate Card 
    path('RateCardTable', views.rateCardTable, name='rateCardTable'),
    path('RateCardTable/<int:clientId>', views.rateCardTable, name='rateCardTableClient'),
    path('RateCardForm/<int:clientId>', views.rateCardForm, name='rateCardForm'),
    # path('RateCardForm/<int:clientId>', views.rateCardForm, name='rateCardWithClient'),
    path('RateCardSave', views.rateCardSave, name='rateCardSave'),
    path('RateCard/view/<int:id>/', views.rateCardForm, name='rateCardView'),
    path('RateCard/revision/<int:id>/', views.rateCardSave, name='rateCardRevision'),
    path('RateCard/revision/<int:id>/<int:edit>/', views.rateCardSave, name='rateCardRevision'),
    path('getOld/rateCards/', views.getOldRateCards, name='getOldRateCards'),
    
    
    # DriverTrip Csv
    path('DriverShiftCsv/', views.driverShiftCsv, name='driverShiftCsv'),
    path('RctiCsvForm/', views.rctiCsvForm, name='rctiCsvForm'),
    path('DriverSampleCsv/', views.driverSampleCsv, name='driverSampleCsv'),
    
    # Edit
    path('driverTrip/edit/<int:id>/', views.DriverTripEditForm, name='DriverTripEdit'), 
    path('driverTrip/update/<int:ids>/', views.driverEntryUpdate, name='driverEntryUpdate'), 
    
    # Filters
    path('verifiedFilter/', views.verifiedFilter, name='verifiedFilter'),  
    path('clientFilter/', views.clientFilter, name='clientFilter'),  
    path('dateRangeFilter/', views.dateRangeFilter, name='dateRangeFilter'),


    # Reconciliation
    path('reconciliation/form/<int:dataType>/', views.reconciliationForm, name='reconciliationForm'),
    path('reconciliation/analysis/<int:dataType>/', views.reconciliationAnalysis, name='reconciliationAnalysis'),
    path('reconciliation/docket/view/<int:docketNumber>/', views.reconciliationDocketView, name='reconciliationDocketView'),
    path('reconciliation/setMark/', views.reconciliationSetMark, name='reconciliationSetMark'),


    # path('docketView/<int:ids>/<int:driverDocketNumber>', views.driverDocketEntry, name='docketView'),      
    path('reconciliationEscalationForm/<int:id>/', views.reconciliationEscalationForm, name='reconciliationEscalationForm'),
    path('reconciliationEscalationForm2/<int:id>/', views.reconciliationEscalationForm2, name='reconciliationEscalationForm2'),
    path('reconciliationEscalationForm3/<int:id>/', views.reconciliationEscalationForm3, name='reconciliationEscalationForm3'),
    path('reconciliationEscalationForm4/<int:id>/', views.reconciliationEscalationForm4, name='reconciliationEscalationForm4'),

    # Public holiday
    path('publicHoliday/', views.publicHoliday, name='publicHoliday'),
    path('publicHoliday/add/', views.publicHolidayForm, name='publicHolidayAdd'),
    path('publicHoliday/add/save/', views.publicHolidaySave, name='publicHolidaySave'),

    path('publicHoliday/edit/<int:id>/', views.publicHolidayForm, name='publicHolidayEdit'),
    path('publicHoliday/edit/save/<int:id>/', views.publicHolidaySave, name='publicHolidayEditSave'),
    
    # Past trip
    path('pastTrip/form/',views.PastTripForm, name='pastTripForm'),
    path('pastTrip/form/save/',views.pastTripSave, name='pastTripSave'),
    path('pastTrip/errorSolve/<int:id>/',views.pastTripErrorSolve, name='pastTripErrorSolve'),
    path('pastTrip/error/resolve/<int:ids>/<int:errorId>/', views.driverDocketEntry, name='pastTripErrorResolve'),
    path('pastTrip/error/get/', views.getSinglePastTripError, name='getSinglePastTripError'),
    
    path('uploded/pastTrip/', views.uplodedPastTrip, name='uplodedPastTrip'),
     
    
    
    # Base plant routes
    path('SurchargeTable/', views.surchargeTable, name='surchargeTable'),
    path('Surcharge/add/', views.surchargeForm, name='surchargeAdd'),
    path('Surcharge/add/save/', views.surchargeSave, name='surchargeAddSave'),   
    path('Surcharge/edit/<int:id>/', views.surchargeForm, name='surchargeEdit'),      
    path('Surcharge/edit/save/<int:id>/', views.surchargeSave, name='surchargeEditSave'),
    
    # Trip 
    path('Driver/Shift/Form/<int:id>', views.DriverShiftForm, name='DriverShiftForm'),
    path('Driver/Shift/Details/<int:id>', views.ShiftDetails, name='ShiftDetails'),

]
