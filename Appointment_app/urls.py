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

app_name = 'Appointment'

urlpatterns = [

    # shifts
    path('create/shift/', views.createShift,name="createShift"),
    path('create/shift/<int:shiftId>/', views.createShift,name="createTrip"),
    path('create/shift/save/', views.createShiftSave,name="createShiftSave"),

    path('create/trip/save/<int:shiftId>/', views.createTripSave,name="createTripSave"),
    # path('start/shift/<str:startDate>/', views.startShift,name="startShiftWithDate"),

    # Appointment
    path('appointmentForm/', views.appointmentForm,name="appointmentForm"),
    path('appointmentForm/view/<int:id>/', views.appointmentForm,name="appointmentFormView"),
    path('appointmentForm/save/', views.appointmentSave,name="appointmentFormSave"),
    
    path('appointmentForm/update/view/<int:id>/<int:update>/', views.appointmentForm,name="appointmentFormUpdateView"),
    path('appointmentForm/update/save/<int:id>/', views.appointmentSave,name="appointmentFormUpdateSave"),

    path('add/stop/view/<int:jobId>/', views.stopView,name="addStopView"),
    path('add/stop/save/<int:jobId>/', views.stopSave,name="addStopSave"),
    
    path('edit/stop/view/<int:stopId>/', views.stopView,name="editStopView"),
    path('edit/stop/save/<int:stopId>/', views.stopSave,name="editStopSave"),
    
    path('findJob/', views.findJob,name="findJob"),
    path('cancelJob/', views.cancelJob,name="cancelJob"),
    
    path('get/driver-appointment/', views.getDriverAppointmentData,name="getDriverAppointment"),
    path('get/single/appointment/', views.getSingleAppointmentData,name="getSingleAppointment"),
    
    path('getTruckAndDriver/', views.getTruckAndDriver ,name="getTruckAndDriver"),
    path('getOriginDetails/', views.getOriginDetails ,name="getOriginDetails"),    
    
    path('pre-start/table/view/', views.preStartTableView ,name="preStartTableView"),    
    path('pre-start/view/<int:id>/', views.preStartForm ,name="preStartView"),
    
    path('pre-start/edit/view/<int:id>/<int:edit>/', views.preStartForm, name="preStartEditView"),
    path('pre-start/edit/save/<int:id>/', views.preStartSave, name="preStartEditSave"),
    path('pre-start/question/swap/', views.swapQueNoSave, name="swapQueNoSave"),
    
    path('pre-start/form/view/', views.preStartForm ,name="preStartForm"),
    path('pre-start/form/save/', views.preStartSave ,name="preStartSave"),

    path('question/add/view/<int:id>/', views.questionAddView ,name="questionAddView"),
    path('question/add/save/<int:id>/', views.questionAddSave ,name="questionAddSave"),

    path('driver/pre-start/table/<int:failed>/', views.driverPreStartTable ,name="driverPreStartTable1"),
    path('driver/pre-start/table/<str:startDate>/<str:endDate>/', views.driverPreStartTable ,name="driverPreStartTable"),
    path('driver/pre-start/table/<str:startDate>/<str:endDate>/<int:failed>/', views.driverPreStartTable ,name="driverFailedPreStartTable"),
    path('driver/pre-start/view/<int:preStartId>/', views.driverPreStartForm ,name="driverPreStartView"),

    path('driver/pre-start/archive/', views.driverPreStartArchive ,name="driverPreStartArchive"),
]