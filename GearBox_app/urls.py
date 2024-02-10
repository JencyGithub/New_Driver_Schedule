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
    # ADD
    path('natureOfLeaveForm/', views.natureOfLeavesForm, name='natureOfLeaveForm'),
    path('natureOfLeaveForm/add/', views.changeNatureOfLeaves, name='addNatureOfLeave'),
    # UPDATE
    path('natureOfLeaves/edit/<int:id>/', views.natureOfLeavesForm, name='natureOfLeavesEdit'), 
    path('natureOfLeaves/edit/save/<int:id>/', views.changeNatureOfLeaves, name='editSaveNatureOfLeaves'), 

    # CRUD Leave Request
    # ADD
    path('leaveReqForm/', views.leaveReqForm, name='leaveReqForm'), 
    path('leaveRequest/add/', views.changeLeaveRequest, name='addLeaveRequest'), 
    # UPDATE
    path('leaveReq/edit/<int:id>/', views.leaveReqForm, name='leaveReqEdit'), 
    path('leaveRequest/edit/save/<int:id>/', views.changeLeaveRequest, name='editSaveLeaveRequest'), 
    
    # Existing Drivers Table + CRUD
    path('drivers/', views.driversView, name='driversTable'),
    
    path('driverForm/', views.driverForm, name='driverFormAdd'),
    path('driverForm/add/', views.driverFormSave, name='driverFormSave'),
    
    path('driverForm/edit/<int:id>/', views.driverForm, name='driverFormEdit'),
    path('driverForm/edit/save/<int:id>/', views.driverFormSave, name='driverFormEditSave'),
    

    # Admin staff 
    path('admin-staff/', views.adminStaffView, name='adminStaffTable'),
    path('admin-staff/add/view/', views.adminStaffForm, name='adminStaffForm'),
    path('admin-staff/add/save/', views.adminStaffSave, name='adminStaffSave'),

    path('admin-staff/edit/view/<int:id>/', views.adminStaffForm, name='adminStaffEdit'),
    path('admin-staff/edit/save/<int:id>/', views.adminStaffSave, name='adminStaffEditSave'),


    # Compliance 
    path('medicalsTable', views.medicalsTable, name='medicalsTable'),
    path('trainingTable', views.trainingTable, name='trainingTable'),

    # Safety
    path('vehicleAccidentsTable', views.vehicleAccidentsTable, name='vehicleAccidentsTable'),
    path('equipmentIssueTable', views.equipmentIssueTable, name='equipmentIssueTable'),

    # Reminder
    path('reminderTable', views.reminderTable, name='reminderTable'),    

    # Truck Table 
    
    path('truckTable', views.truckTable, name='truckTable'),
    path('truckForm', views.truckForm, name='truckForm'),
    path('truckForm/add/', views.truckFormSave, name='truckFormSave'),
    path('truckForm/update/<int:truckId>', views.truckFormSave, name='truckFormUpdate'),
    
    path('truckForm/Axles/View/<int:truckId>', views.truckAxlesFormView, name='truckAxlesFormView'),
    path('truckForm/Axles/Save/<int:truckId>', views.truckAxlesFormSave, name='truckAxlesFormSave'),
    
    path('truckForm/Setting/View/<int:truckId>', views.truckSettingFormView, name='truckSettingFormView'),
    path('truckForm/Setting/Save', views.truckSettingFormSave, name='truckSettingFormSave'),
    
    path('truckForm/Reminders/View', views.truckRemindersFormView, name='truckRemindersFormView'),
    path('truckForm/Reminders/Save', views.truckRemindersFormSave, name='truckRemindersFormSave'),
    
    path('truckForm/Parts/View', views.truckPartsFormView, name='truckPartsFormView'),
    path('truckForm/Parts/Save', views.truckPartsFormSave, name='truckPartsFormSave'),
    
    path('truckForm/History/View', views.truckHistoryFormView, name='truckHistoryFormView'),
    path('truckForm/History/Save', views.truckHistoryFormSave, name='truckHistoryFormSave'),
    
    path('truckForm/Odometer/View', views.truckOdometerFormView, name='truckOdometerFormView'),
    path('truckForm/Odometer/Save', views.truckOdometerFormSave, name='truckOdometerFormSave'),
    
    path('truckForm/Compliance/View', views.truckComplianceFormView, name='truckComplianceFormView'),
    path('truckForm/Compliance/Save', views.truckComplianceFormSave, name='truckComplianceFormSave'),
    
    path('truckForm/Documents/View', views.truckDocumentsFormView, name='truckDocumentsFormView'),
    path('truckForm/Documents/Save', views.truckDocumentsFormSave, name='truckDocumentsFormSave'),
    
    path('truck/view/<int:id>/', views.truckForm, name='truckView'),
    
    
    path('truckConnection/add/view/<int:id>/', views.truckConnectionForm, name='truckConnectionAddView'),
    path('truckConnection/add/save/<int:id>/', views.truckConnectionSave, name='truckConnectionSaveView'),
    path('getRateCard/', views.getRateCard, name='getRateCard'),
    
    # dockument 
    # path('document/', views.documentView, name="do

    # truck setting form 
    path("settingsForm/", views.settingsForm, name="settingsForm"),

    # Compliance form 
    path("complianceForm/", views.complianceForm, name="complianceForm"),

    # Client Table
    
    path('clientTable', views.clientTable, name='clientTable'),
    
    path('client/add/', views.clientForm, name='clientAdd'),
    path('client/add/save/', views.clientChange, name='clientAddSave'),
    
    path('client/edit/<int:id>/', views.clientForm, name='clientEdit'),
    path('client/edit/save/<int:id>/', views.clientChange, name='clientEditSave'),

    # Groups

    path('truck/groups/view', views.groupsView, name='groupsView'),
    path('truck/groups/add/save/', views.addGroupsSave, name='addGroupsSave'),

    # Sub groups 
    path('subgroups/add/', views.addSubGroups, name='addSubGroups'),

    # Fleet Settings 
    path('fleet/Settings/', views.fleetSettings, name='fleetSettings'),    
    path('fleet/customInformation/save', views.fleetCustomInformationSave, name='fleetCustomInformationSave'),    
]