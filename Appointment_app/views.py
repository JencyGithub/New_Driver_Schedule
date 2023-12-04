from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import shutil ,os ,subprocess ,csv
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib import messages
from Account_app.models import *
from GearBox_app.models import *
from Appointment_app.models import *
from django.http import FileResponse
from CRUD import *
from Account_app.reconciliationUtils import *
from django.db.models import Q
import itertools

# ````````````````````````````````````
# Appointment

# ```````````````````````````````````

def convertDateTimeForTemplate(provided_date_string):
    datetime_obj = datetime.strptime(str(provided_date_string), "%Y-%m-%d %H:%M:%S%z")
    formatted_datetime = datetime_obj.strftime("%Y-%m-%dT%H:%M")
    return formatted_datetime

def appointmentForm(request, id=None):
    drivers = Driver.objects.all()
    clients = Client.objects.all()
    truckNos = AdminTruck.objects.all()
    params = {
        'drivers' : drivers,
        'truckNos':truckNos,
        'clients' : clients,   
    }
    if id:
        data = Appointment.objects.filter(pk=id).first()
        data.Start_Date_Time = convertDateTimeForTemplate(data.Start_Date_Time)
        data.End_Date_Time = convertDateTimeForTemplate(data.End_Date_Time)
        data.report_to_origin = convertDateTimeForTemplate(data.report_to_origin)
        data.Report_Time = str(data.Report_Time)
        data.Dwell_Time = str(data.Dwell_Time)
        data.Block_Time = str(data.Block_Time)
        data.Total_Time = str(data.Total_Time)
        params['data'] = data
    return render(request, 'Appointment/appointmentForm.html',params)

@csrf_protect
@api_view(['POST'])
def applicationSave(request):
    driver = Driver.objects.filter(pk=request.POST.get('driverName')).first()
    client = Client.objects.filter(pk=request.POST.get('stopName')).first()

    appointmentObj = Appointment()
    appointmentObj.Title = request.POST.get('title')
    appointmentObj.Start_Date_Time = request.POST.get('startDateTime')
    appointmentObj.End_Date_Time = request.POST.get('endDateTime')
    appointmentObj.report_to_origin = request.POST.get('reportToOrigin')
    appointmentObj.Status = request.POST.get('status')
    appointmentObj.Origin = request.POST.get('origin')
    appointmentObj.Recurring = request.POST.get('recurring')
    appointmentObj.Staff_Notes = request.POST.get('staffNotes')
    appointmentObj.Created_by = request.POST.get('createdBy')
    # appointmentObj.Created_time = request.POST.get('Created_time')
    appointmentObj.Report_Time = request.POST.get('reportTime')
    appointmentObj.Dwell_Time = request.POST.get('dwellTime')
    appointmentObj.Block_Time = request.POST.get('blockTime')
    appointmentObj.Total_Time = request.POST.get('totalTime')
    appointmentObj.truckNo = request.POST.get('truckNo')
    appointmentObj.driver = driver
    appointmentObj.stop = client
    
    appointmentObj.save()
    
    messages.success(request, "Form Successfully Filled Up.")
    return redirect(request.META.get('HTTP_REFERER'))

def findJob(request):
    jobs = Appointment.objects.filter(scheduled = False)
    params = {
        'jobs' : jobs
    }
    return render(request, 'Appointment/findJob.html',params)

@csrf_protect
def getTruckAndDriver(request):
    startDateTime = request.POST.get('startDateTime')
    endDateTime = request.POST.get('endDateTime')
    print(startDateTime,endDateTime)
    
    startDateTime = datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M')
    endDateTime = datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M')
        
    # Qry logic
    # Appointment.objects.get(Q(Start_Date_Time__gte = startDateTime,Start_Date_Time__lte = endDateTime)|Q(End_Date_Time__gte = startDateTime,End_Date_Time__lte = endDateTime))
    #                               03-04              01-04            03-04            04-04               02-04             01-04              02-04             04-04                   
    # job = 1-4, 4-4        Data from form
    # d1 = 25-3 , 02-4      Entry from database
    # d2 = 03-4 , 10-4      Entry from database
    
    
    unavailableDriversAndTrucksQrySet = Appointment.objects.filter(Q(Start_Date_Time__gte = startDateTime,Start_Date_Time__lte = endDateTime)|Q(End_Date_Time__gte = startDateTime,End_Date_Time__lte = endDateTime))
    unavailableDriversQrySet = [] 
    unavailableTrucksQrySet = [] 

    for obj in unavailableDriversAndTrucksQrySet:
        tempDriver = obj.driver
        tempTruck = AdminTruck.objects.filter(adminTruckNumber = obj.truckNo).first()
        unavailableDriversQrySet.append({'driverId':tempDriver.driverId,'name':tempDriver.name})
        unavailableTrucksQrySet.append({'adminTruckNumber':tempTruck.adminTruckNumber})

    drivers = Driver.objects.values('driverId','name')
    trucks =  AdminTruck.objects.values('adminTruckNumber')

    availableDriversList = list(itertools.filterfalse(lambda x: x in list(drivers), unavailableDriversQrySet)) + list(itertools.filterfalse(lambda x: x in unavailableDriversQrySet, list(drivers)))
    availableTrucksList = list(itertools.filterfalse(lambda x: x in list(trucks), unavailableTrucksQrySet)) + list(itertools.filterfalse(lambda x: x in unavailableTrucksQrySet, list(trucks)))

    # availableTrucksList = list(set(trucks.items()) - set(unavailableTrucksQrySet))
    # availableDriversList = list(set(drivers.items()) - set(unavailableDriversQrySet.items()))

    return JsonResponse({'status': True, 'availableTrucksList': availableTrucksList, 'availableDriversList': availableDriversList})

    # Add logic for leave request here
    
   


