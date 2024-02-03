from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import shutil, os, subprocess, csv, pytz
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

def appointmentForm(request, id=None, update=None):
    currentUser = request.user
    drivers = Driver.objects.all()
    clients = Client.objects.all()
    truckNos = AdminTruck.objects.all()
    params = {
        'drivers' : drivers,
        'truckNos':truckNos,
        'clients' : clients,  
        'currentUser' : currentUser 
    }
    if id:
        data = Appointment.objects.filter(pk=id).first()
        data.Start_Date_Time = convertDateTimeForTemplate(data.Start_Date_Time)
        data.End_Date_Time = convertDateTimeForTemplate(data.End_Date_Time)
        data.report_to_origin = convertDateTimeForTemplate(data.report_to_origin)
        
        appointmentDriver = AppointmentDriver.objects.filter(appointmentId = data.id).last()
        appointmentTruck = AppointmentTruck.objects.filter(appointmentId = data.id).last()

        params['data'] = data
        params['appointmentDriver'] = appointmentDriver
        params['appointmentTruck'] = appointmentTruck
        
        unavailableDriversAndTrucksQrySet = Appointment.objects.filter(Q(Start_Date_Time__gte = data.Start_Date_Time,Start_Date_Time__lte = data.End_Date_Time)|Q(End_Date_Time__gte = data.Start_Date_Time,End_Date_Time__lte = data.End_Date_Time))
        unavailableDriversQrySet = [] 
        unavailableTrucksQrySet = [] 
        

        for obj in unavailableDriversAndTrucksQrySet:            
            tempDriver = AppointmentDriver.objects.filter(appointmentId = obj.id).last()
            tempTruck = AppointmentTruck.objects.filter(appointmentId = obj.id).last()
            if tempDriver:
                unavailableDriversQrySet.append({'driverId':tempDriver.driverName.driverId,'name':tempDriver.driverName.name})
            if tempTruck:
                unavailableTrucksQrySet.append({'adminTruckNumber':tempTruck.truckNo.adminTruckNumber})

        drivers = Driver.objects.values('driverId','name')
        trucks =  AdminTruck.objects.values('adminTruckNumber')

        availableDriversList = list(itertools.filterfalse(lambda x: x in list(drivers), unavailableDriversQrySet)) + list(itertools.filterfalse(lambda x: x in unavailableDriversQrySet, list(drivers)))
        availableTrucksList = list(itertools.filterfalse(lambda x: x in list(trucks), unavailableTrucksQrySet)) + list(itertools.filterfalse(lambda x: x in unavailableTrucksQrySet, list(trucks)))
        
        
        params['availableDriversList'] = availableDriversList
        params['availableTrucksList'] = availableTrucksList
        params['update'] = update
        
        print(availableDriversList,availableTrucksList)
        
        
    return render(request, 'Appointment/appointmentForm.html',params)

@csrf_protect
def appointmentSave(request,id=None):
    appointmentObj = Appointment()
    if id:
        appointmentObj = Appointment.objects.filter(pk=id).first()
        messageStr = "Appointment Updated Successfully."
    else:
    # if not id:
        client = Client.objects.filter(pk=request.POST.get('stopName').strip()).first()
        newOrigin = request.POST.get('originAddVal').strip()
        originObj = None
        if newOrigin == 1:
            originObj = BasePlant()
            originObj.basePlant = request.POST.get('origin')
            originObj.address = request.POST.get('originAddress')
            originObj.phone = request.POST.get('originPhone')
            originObj.personOnName = request.POST.get('originPersonOnName')
            originObj.managerName = request.POST.get('originPersonOnName')
            originObj.lat = request.POST.get('originLatitude')
            originObj.long = request.POST.get('originLongitude')
            originObj.save()
        else:
            originObj = BasePlant.objects.filter(basePlant=request.POST.get('origin').upper().strip()).first()

        appointmentObj.Title = request.POST.get('title')
        appointmentObj.Start_Date_Time = request.POST.get('startDateTime')
        appointmentObj.End_Date_Time = request.POST.get('endDateTime')
        appointmentObj.report_to_origin = request.POST.get('reportToOrigin')
        appointmentObj.Recurring = request.POST.get('recurring')
        appointmentObj.Staff_Notes = request.POST.get('staffNotes')
        appointmentObj.Created_by = request.user
        appointmentObj.stop = client
        appointmentObj.Origin = originObj
        appointmentObj.shiftType = request.POST.get('shiftType')
        appointmentObj.Status = 'Unassigned'
        appointmentObj.save()
        messageStr = "Appointment added successfully."
    
    driver = Driver.objects.filter(pk=request.POST.get('driverName')).first()
    if driver:
        appointmentDriverObj = AppointmentDriver.objects.filter(appointmentId = appointmentObj.id).first()
        if not appointmentDriverObj:
            appointmentDriverObj = AppointmentDriver()
            
        appointmentDriverObj.driverName = driver
        appointmentDriverObj.appointmentId = appointmentObj
        appointmentDriverObj.save()
    
    truck = AdminTruck.objects.filter(adminTruckNumber=request.POST.get('truckNo')).first()

    if truck:
        appointmentTruckObj = AppointmentTruck.objects.filter(appointmentId = appointmentObj.id).first()
        if not appointmentTruckObj:
            appointmentTruckObj = AppointmentTruck()
            
        appointmentTruckObj.truckNo = truck
        appointmentTruckObj.appointmentId = appointmentObj
        appointmentTruckObj.save()
        
    if driver and truck:
        appointmentObj.Status = "Assigned"
        appointmentObj.save()
        
    messages.success(request, messageStr)

    return redirect('Appointment:findJob')        

def findJob(request):
    return render(request, 'Appointment/findJob.html')

@csrf_protect
@api_view(['POST'])
def cancelJob(request):
    appointmentId = request.POST.get('appointmentId') 
    appointmentObj = Appointment.objects.filter(pk=appointmentId).first()
    if appointmentObj:
        appointmentObj.Status = 'Cancelled'
        appointmentObj.save()
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False})


@csrf_protect
@api_view(['POST'])
def getDriverAppointmentData(request):
    appointments = []
    selectedJobs = request.POST.getlist('selectedStatus[]')
    if len(selectedJobs) > 0:
        appointments = Appointment.objects.filter(Status__in=selectedJobs)
    else:
        appointments = Appointment.objects.all()
        
    drivers = Driver.objects.all()

    appointmentsList = []
    for job in appointments:
        appointment_data = {
            'id' : job.id,
            'start': str(job.Start_Date_Time).split('+')[0],
            'end': str(job.End_Date_Time).split('+')[0],
            'title': str(job.Title),
            'status': str(job.Status),
        }
        driver = AppointmentDriver.objects.filter(appointmentId=job).first()
        if driver:
            appointment_data["resourceId"] = driver.driverName.driverId
            appointment_data["driverName"] = driver.driverName.name
        appointmentsList.append(appointment_data)
    driversList = [{'id': driver.driverId, 'title': driver.name} for driver in drivers]
    return JsonResponse({'status': True, 'appointments': appointmentsList, 'drivers': driversList})
    
@csrf_protect
@api_view(['POST'])
def getSingleAppointmentData(request):
    appointmentId = request.POST.get('appointmentId')
    appointmentObj = Appointment.objects.filter(pk=appointmentId).values().first()
    appointmentObj['Created_by_id'] = User.objects.filter(pk=appointmentObj['Created_by_id']).first().username
    originObj = BasePlant.objects.filter(pk=appointmentObj['Origin_id']).values().first()
    appointmentObj['Origin_id'] = originObj['basePlant']

    driverObj = AppointmentDriver.objects.filter(appointmentId=appointmentObj['id']).values().first()
    driverObj = Driver.objects.filter(pk=driverObj['driverName_id']).values().first()

    truckObj = AppointmentTruck.objects.filter(appointmentId=appointmentObj['id']).values().first()
    truckObj = AdminTruck.objects.filter(pk=truckObj['truckNo_id']).values().first()

    return JsonResponse({'status': True, 'appointmentObj': appointmentObj, 'driverObj': driverObj, 'truckObj': truckObj, 'originObj': originObj})
    
    
@csrf_protect
def getTruckAndDriver(request):
    startDateTime = request.POST.get('startDateTime')
    endDateTime = request.POST.get('endDateTime')
    
    print(startDateTime,endDateTime)
    
    try:
        startDateTime = datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S')
        endDateTime = datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S')
    except ValueError as e:
        startDateTime =  datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M')
        endDateTime =  datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M')
        
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
        # tempDriver = obj.driver
        # tempTruck = AdminTruck.objects.filter(adminTruckNumber = obj.truckNo).first()
        
        tempDriver = AppointmentDriver.objects.filter(appointmentId = obj.id).first()
        tempTruck = AppointmentTruck.objects.filter(appointmentId = obj.id).first()
        if tempDriver:
            unavailableDriversQrySet.append({'driverId':tempDriver.driverName.driverId,'name':tempDriver.driverName.name})
        if tempTruck:
            unavailableTrucksQrySet.append({'adminTruckNumber':tempTruck.truckNo.adminTruckNumber})

    drivers = Driver.objects.values('driverId','name')
    trucks =  AdminTruck.objects.values('adminTruckNumber')

    availableDriversList = list(itertools.filterfalse(lambda x: x in list(drivers), unavailableDriversQrySet)) + list(itertools.filterfalse(lambda x: x in unavailableDriversQrySet, list(drivers)))
    availableTrucksList = list(itertools.filterfalse(lambda x: x in list(trucks), unavailableTrucksQrySet)) + list(itertools.filterfalse(lambda x: x in unavailableTrucksQrySet, list(trucks)))

    return JsonResponse({'status': True, 'availableTrucksList': availableTrucksList, 'availableDriversList': availableDriversList})

    # Add logic for leave request here
    

@csrf_protect
def getOriginDetails(request):
    originName = request.POST.get('originName').strip().upper()
    status = True
    origin = BasePlant.objects.filter(basePlant=originName).values().first()
    print(originName,origin)
    if not origin:
        status = False
    return JsonResponse({'status': status ,'origin' : origin})

def preStartTableView(request):
    preStarts = PreStart.objects.all()
    params = {'preStarts':preStarts}
    return render(request, 'Appointment/preStartTable.html', params)

def preStartForm(request, id=None):
    if id:
        data = PreStart.objects.filter(pk=id).first()
        questions = PreStartQuestion.objects.filter(preStartId=data.id)
        params = {
            'data' : data,
            'questions' : questions,
            'queLen' : len(questions)    
        }
    else:
        params = {}
    return render(request, 'Appointment/preStartForm.html', params)

@csrf_protect
def preStartSave(request):
    currentTimezone = pytz.timezone('Asia/Kolkata')
    currentDateTime = datetime.now(tz=currentTimezone)
    preStartName = request.POST.get('preStartName')
    questionCount = request.POST.get('queCount')
    
    preStartObj = PreStart()
    preStartObj.preStartName = preStartName
    preStartObj.createdDate = currentDateTime
    preStartObj.createdBy = request.user
    preStartObj.save()
    for question in range(1,int(questionCount)):
        questionObj = PreStartQuestion()
        questionObj.preStartId = preStartObj
        questionObj.questionText = request.POST.get(f'q{question}txt')
        questionObj.questionType = request.POST.get(f'q{question}type')
        
        queTxt1 = request.POST.get(f'q{question}o1')
        queTxt2 = request.POST.get(f'q{question}o2')
        queTxt3 = request.POST.get(f'q{question}o3')
        queTxt4 = request.POST.get(f'q{question}o4')
        wantFile = request.POST.get(f'wantFile{question}')
        
        questionObj.optionTxt1 = queTxt1
        
        if queTxt2:
            questionObj.optionTxt2 = request.POST.get(f'q{question}o2')
        if queTxt3:
            questionObj.optionTxt3 = request.POST.get(f'q{question}o3')
        if queTxt4:
            questionObj.optionTxt4 = request.POST.get(f'q{question}o4')

        if wantFile == f'q{question}o1wantFile':
            questionObj.wantFile1 = True
        elif wantFile == f'q{question}o2wantFile':
            questionObj.wantFile2 = True
        elif wantFile == f'q{question}o3wantFile':
            questionObj.wantFile3 = True
        elif wantFile == f'q{question}o4wantFile':
            questionObj.wantFile4 = True
            
        questionObj.save()

    messages.success(request, "Pre-start added.")
    return redirect('Appointment:preStartTableView')
    

def questionAddView(request, id):
    preStartObj = PreStart.objects.filter(pk=id).first()

    params = {'data':preStartObj}
    return render(request, 'Appointment/addPre-startQuestion.html', params)
    
@csrf_protect
def questionAddSave(request, id):
    preStartObj = PreStart.objects.filter(pk=id).first()
    questionObj = PreStartQuestion()
    questionObj.preStartId = preStartObj
    
    questionObj.questionText = request.POST.get("quetxt")
    questionObj.questionType = request.POST.get("quetype")
    
    queTxt1 = request.POST.get('opt1')
    queTxt2 = request.POST.get('opt2')
    queTxt3 = request.POST.get('opt3')
    queTxt4 = request.POST.get('opt4')
    wantFile = request.POST.get('wantFile')
    questionObj.optionTxt1 = queTxt1
    
    if queTxt2:
        questionObj.optionTxt2 = queTxt2
    if queTxt3:
        questionObj.optionTxt3 = queTxt3
    if queTxt4:
        questionObj.optionTxt4 = queTxt4
        
    if wantFile == 'opt1wantFile':
        questionObj.wantFile1 = True
    elif wantFile == 'opt2wantFile':
        questionObj.wantFile2 = True
    elif wantFile == 'opt3wantFile':
        questionObj.wantFile3 = True
    elif wantFile == 'opt4wantFile':
        questionObj.wantFile4 = True
        
    questionObj.save()
    
    messages.success(request, "Question added.")
    return redirect('Appointment:preStartTableView')

