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
    trucks = AdminTruck.objects.all()
    origins = BasePlant.objects.all()
    curDate = getCurrentDateTimeObj().date()

    params = {
        'drivers' : drivers,
        'trucks':trucks,
        'clients' : clients,  
        'currentUser' : currentUser,
        'origins' : origins,
        'curDate' : str(curDate)
    }
    if id:
        data = Appointment.objects.filter(pk=id).first()
        data.startTime = str(data.startTime)
        data.endTime = str(data.endTime)
        data.reportingTime = str(data.reportingTime)
        data.startDate = dateConverterFromTableToPageFormate(data.startDate)
        data.endDate = dateConverterFromTableToPageFormate(data.endDate)
        
        appointmentDriver = AppointmentDriver.objects.filter(appointmentId = data.id).last()
        appointmentTruck = AppointmentTruck.objects.filter(appointmentId = data.id).last()
        appointmentStop = AppointmentStop.objects.filter(appointmentId = data.id).last()

        params['data'] = data
        params['appointmentDriver'] = appointmentDriver
        params['appointmentTruck'] = appointmentTruck
        params['appointmentStop'] = appointmentStop
        
        # unavailableDriversAndTrucksQrySet = Appointment.objects.filter(Q(startTime__gte = data.startTime,startTime__lte = data.endTime)|Q(endTime__gte = data.startTime,endTime__lte = data.endTime))
        # unavailableDriversQrySet = [] 
        # unavailableTrucksQrySet = [] 
        
        # for obj in unavailableDriversAndTrucksQrySet:            
        #     tempDriver = AppointmentDriver.objects.filter(appointmentId = obj.id).last()
        #     tempTruck = AppointmentTruck.objects.filter(appointmentId = obj.id).last()
        #     if tempDriver:
        #         unavailableDriversQrySet.append({'driverId':tempDriver.driverName.driverId,'name':tempDriver.driverName.name})
        #     if tempTruck:
        #         unavailableTrucksQrySet.append({'adminTruckNumber':tempTruck.truckNo.adminTruckNumber})

        # drivers = Driver.objects.values('driverId','name')
        # trucks =  AdminTruck.objects.values('adminTruckNumber')

        # availableDriversList = list(itertools.filterfalse(lambda x: x in list(drivers), unavailableDriversQrySet)) + list(itertools.filterfalse(lambda x: x in unavailableDriversQrySet, list(drivers)))
        # availableTrucksList = list(itertools.filterfalse(lambda x: x in list(trucks), unavailableTrucksQrySet)) + list(itertools.filterfalse(lambda x: x in unavailableTrucksQrySet, list(trucks)))

        availableDriversList = AdminTruck.objects.all()
        availableTrucksList = Driver.objects.all()
        params['availableDriversList'] = availableDriversList
        params['availableTrucksList'] = availableTrucksList
        params['update'] = update
    # return HttpResponse(params)
    return render(request, 'Appointment/appointmentForm.html',params)

@csrf_protect
def appointmentSave(request,id=None):
    appointmentObj = Appointment()
    recurringType = request.POST.get('repeats')
    startTime = request.POST.get('startTime')
    endTime = request.POST.get('endTime')
    shiftDate = request.POST.get('shiftDate')
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    reportingTime = request.POST.get('reportingTime')
    shiftType = None
    
    if 6 <= int(startTime.split(':')[0]) <= 17 :
        shiftType = "Day"
    else:
        shiftType = "Night"

    if id:
        appointmentObj = Appointment.objects.filter(pk=id).first()
        messageStr = "Appointment Updated Successfully."
    else:
        client = Client.objects.filter(pk=request.POST.get('stopName').strip()).first()
        # newOrigin = request.POST.get('originAddVal').strip()
        # if newOrigin == 1:
        #     originObj = BasePlant()
        #     originObj.basePlant = request.POST.get('origin')
        #     originObj.address = request.POST.get('originAddress')
        #     originObj.phone = request.POST.get('originPhone')
        #     originObj.personOnName = request.POST.get('originPersonOnName')
        #     originObj.managerName = request.POST.get('originPersonOnName')
        #     originObj.lat = request.POST.get('originLatitude')
        #     originObj.long = request.POST.get('originLongitude')
        #     originObj.save()
        
        


        appointmentObj.title = request.POST.get('title')
        appointmentObj.recurringType = recurringType
        appointmentObj.startTime = startTime
        appointmentObj.endTime = endTime
        appointmentObj.reportingTime = reportingTime
        appointmentObj.createdBy = request.user
        appointmentObj.stop = client
        appointmentObj.staffNotes = request.POST.get('staffNotes')
        appointmentObj.driverNotes = request.POST.get('driverNotes')
        appointmentObj.shiftType = shiftType
        appointmentObj.status = 'Unassigned'
        
        if recurringType == 'NoRecurring':
            appointmentObj.startDate = shiftDate
            appointmentObj.endDate = shiftDate
        else:
            appointmentObj.startDate = startDate
            appointmentObj.endDate = endDate
            if recurringType == 'Custom':
                check_day = lambda day_input, condition_value: True if day_input == condition_value else False
                appointmentObj.sunday = check_day(request.POST.get('sunday'), 'sunday')
                appointmentObj.monday = check_day(request.POST.get('monday'), 'monday')
                appointmentObj.tuesday = check_day(request.POST.get('tuesday'), 'tuesday')
                appointmentObj.wednesday = check_day(request.POST.get('wednesday'), 'wednesday')
                appointmentObj.thursday = check_day(request.POST.get('thursday'), 'thursday')
                appointmentObj.friday = check_day(request.POST.get('friday'), 'friday')
                appointmentObj.saturday = check_day(request.POST.get('saturday'), 'saturday')
        
        appointmentObj.save()
        messageStr = "Appointment added successfully."
        
    # Add origin
    originId = request.POST.get('origin')
    if originId:
        originObj = BasePlant.objects.filter(pk=originId).first()
        appointmentObj.origin = originObj
        appointmentObj.save()
    
    # Add driver
    driver = Driver.objects.filter(pk=request.POST.get('driverName')).first()
    if driver:
        appointmentDriverObj = AppointmentDriver.objects.filter(appointmentId = appointmentObj.id).first()
        if not appointmentDriverObj:
            appointmentDriverObj = AppointmentDriver()
            
        appointmentDriverObj.driverName = driver
        appointmentDriverObj.appointmentId = appointmentObj
        appointmentDriverObj.save()
    # Add truck
    truck = AdminTruck.objects.filter(pk=request.POST.get('truckNo')).first()    
    if truck:
        appointmentTruckObj = AppointmentTruck.objects.filter(appointmentId = appointmentObj.id).first()
        if not appointmentTruckObj:
            appointmentTruckObj = AppointmentTruck()
            
        appointmentTruckObj.truckNo = truck
        appointmentTruckObj.appointmentId = appointmentObj
        appointmentTruckObj.save()
    # Add stop
    
    stopName = BasePlant.objects.filter(pk=request.POST.get('appStop')).first()
    if stopName:
        appointmentStopObj = AppointmentStop()
        appointmentStopObj.stopName = stopName
        appointmentStopObj.appointmentId = appointmentObj
        appointmentStopObj.save()
   
        
    if driver and truck:
        appointmentObj.status = "Assigned"
        appointmentObj.save()
        
    messages.success(request, messageStr)

    return redirect('Appointment:findJob')        

@csrf_protect
def findJob(request):
    drivers = Driver.objects.all().order_by('name')
    vehicles = AdminTruck.objects.all().order_by('adminTruckNumber')
    locations = BasePlant.objects.all().order_by('basePlant')
    
    params = {
        'drivers' : drivers,
        'vehicles' : vehicles,
        'locations' : locations
    }
    return render(request, 'Appointment/findJob.html', params)

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
def getSingleAppointmentData(request):
    appointmentId = request.POST.get('appointmentId')
    appointmentObj = Appointment.objects.filter(pk=appointmentId).values().first()
    appointmentObj['createdBy_id'] = User.objects.filter(pk=appointmentObj['createdBy_id']).first().username
    
    originObj = BasePlant.objects.filter(pk=appointmentObj['origin_id']).values().first()
    if originObj:
        appointmentObj['origin_id'] = originObj['basePlant']
        
    appointmentObj['clientName'] = Client.objects.filter(pk = appointmentObj['stop_id']).first().name

    stopObj = AppointmentStop.objects.filter(appointmentId=appointmentObj['id']).first()
    if stopObj:
        stopObj = BasePlant.objects.filter(pk=stopObj.stopName.id).values().first()

    driverObj = AppointmentDriver.objects.filter(appointmentId=appointmentObj['id']).values().first()
    if driverObj:
        driverObj = Driver.objects.filter(pk=driverObj['driverName_id']).values().first()

    truckObj = AppointmentTruck.objects.filter(appointmentId=appointmentObj['id']).values().first()
    if truckObj:
        truckObj = AdminTruck.objects.filter(pk=truckObj['truckNo_id']).values().first()

    return JsonResponse({'status': True, 'appointmentObj': appointmentObj, 'driverObj': driverObj, 'truckObj': truckObj, 'originObj': originObj, 'stopObj': stopObj})
    
    
@csrf_protect
def getTruckAndDriver(request):
    startDateTime = request.POST.get('startDateTime')
    endDateTime = request.POST.get('endDateTime')
    
    try:
        startDateTime = datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S')
        endDateTime = datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S')
    except ValueError as e:
        startDateTime =  datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M')
        endDateTime =  datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M')
        
    # Qry logic
    # Appointment.objects.get(Q(startTime__gte = startDateTime,startTime__lte = endDateTime)|Q(endTime__gte = startDateTime,endTime__lte = endDateTime))
    #                               03-04              01-04            03-04            04-04               02-04             01-04              02-04             04-04                   
    # job = 1-4, 4-4        Data from form
    # d1 = 25-3 , 02-4      Entry from database
    # d2 = 03-4 , 10-4      Entry from database
    
    
    unavailableDriversAndTrucksQrySet = Appointment.objects.filter(Q(startTime__gte = startDateTime,startTime__lte = endDateTime)|Q(endTime__gte = startDateTime,endTime__lte = endDateTime))
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
    originId = request.POST.get('originName').strip().upper()
    status = True
    origin = BasePlant.objects.filter(pk=originId).values().first()
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


@csrf_protect
@api_view(['POST'])
def getDriverAppointmentData(request):
    appointments = []
    selectedJobs = request.POST.getlist('selectedStatus[]')
    selectedDrivers = request.POST.getlist('selectedDrivers[]')
    selectedLocations = request.POST.getlist('selectedLocations[]')
    selectedVehicles = request.POST.getlist('selectedVehicles[]')
    selectedContents = request.POST.getlist('selectedContents[]')
    
    appointments = Appointment.objects.all()
    drivers = None
    
    if len(selectedDrivers) > 0:
        selectedDrivers = [int(item.replace('driver', '')) for item in selectedDrivers]
        drivers = Driver.objects.filter(pk__in=selectedDrivers)
    else:
        drivers = Driver.objects.all()
        
    if len(selectedLocations) > 0:
        selectedLocations = [int(item.replace('location', '')) for item in selectedLocations]

    if len(selectedVehicles) > 0:
        selectedVehicles = [int(item.replace('vehicle', '')) for item in selectedVehicles]
    
    
    if len(selectedLocations) > 0 and len(selectedJobs) > 0 and len(selectedVehicles) > 0:
        appointments = Appointment.objects.filter(appointmenttruck__truckNo__id__in=selectedVehicles, origin__id__in=selectedLocations, status__in=selectedJobs)        
    elif len(selectedLocations) > 0 and len(selectedVehicles) > 0:
        appointments = Appointment.objects.filter(appointmenttruck__truckNo__id__in=selectedVehicles, origin__id__in=selectedLocations)        
    elif len(selectedJobs) > 0 and len(selectedVehicles) > 0:
        appointments = Appointment.objects.filter(appointmenttruck__truckNo__id__in=selectedVehicles, status__in=selectedJobs)        
    elif len(selectedLocations) > 0 and  len(selectedJobs) > 0:
        appointments = Appointment.objects.filter(origin__id__in=selectedLocations, status__in=selectedJobs)
    elif len(selectedJobs) > 0:
        appointments = Appointment.objects.filter(status__in=selectedJobs)
    elif len(selectedLocations) > 0:
        appointments = Appointment.objects.filter(origin__id__in=selectedLocations)
    elif len(selectedVehicles) > 0:
        appointments = Appointment.objects.filter(appointmenttruck__truckNo__id__in=selectedVehicles)        
    
    appointmentsList = []
    
    def addJob(startDate, endDate, data, driverData, contents):
        titleData = [f'{str(data.startTime)}-{str(data.endTime)}']

        if len(contents) > 0:
            if 'timeContent' not in contents:
                titleData = []
            if 'driverContent' in contents and driverData:
                print("driverData", driverData.driverName.name)
                titleData.append(driverData.driverName.name)
            if 'titleContent' in contents:
                titleData.append(data.title)
            if 'customerContent' in contents:
                titleData.append(data.stop.name)
            if 'staffNotesContent' in contents:
                titleData.append(data.staffNotes)
            if 'driverNotesContent' in contents:
                titleData.append(data.driverNotes)
            if 'reportingTimeContent' in contents:
                titleData.append(data.reportingTime)
            if 'shiftTypeContent' in contents:
                titleData.append(data.shiftType)
            if 'createdByContent' in contents:
                titleData.append(data.createdBy.username)
            if 'crestedTimeContent' in contents:
                titleData.append(data.createdTime)
            if 'addressContent' in contents:
                titleData.append(data.origin.address)
                
            if 'vehicleContent' in contents:                    
                vehicleInfo = AppointmentTruck.objects.filter(appointmentId=data).first()
                if vehicleInfo:
                    titleData.append(vehicleInfo.truckNo.adminTruckNumber)
                
        dataDict = {
            'id': data.id,
            'start': str(startDate) + ' ' + str(data.startTime),
            'end': str(endDate) + ' ' + str(data.endTime),
            'title': titleData,
            'status': str(data.status)
        }
        if driverData:
            dataDict["resourceId"] = driver.driverName.driverId
            dataDict["driverName"] = driver.driverName.name
        else:
            dataDict["resourceId"] = 0
            dataDict["driverName"] = 'Unassigned'
        
            
        return dataDict
    
    for job in appointments:
        driver = AppointmentDriver.objects.filter(appointmentId=job).first()
        
        if job.recurringType == "NoRecurring":
            appointmentsList.append(addJob(startDate=job.startDate, endDate=job.endDate, data=job, driverData = driver, contents=selectedContents))
            
        elif job.recurringType == "Daily":
            current_date = job.startDate
            while current_date <= job.endDate:
                appointmentsList.append(addJob(startDate=current_date, endDate=current_date, data=job, driverData = driver, contents=selectedContents))
                current_date += timedelta(days=1)

        elif  job.recurringType == "Custom":
            weekdays = []            
            current_date = job.startDate
            
            dayCheck = lambda val, number: weekdays.append(number) if val else None
            dayCheck(job.monday, 0)
            dayCheck(job.tuesday, 1)
            dayCheck(job.wednesday, 2)
            dayCheck(job.thursday, 3)
            dayCheck(job.friday, 4)
            dayCheck(job.saturday, 5)
            dayCheck(job.sunday, 6)
                
            while current_date <= job.endDate:
                if current_date.weekday() in weekdays:
                    appointmentsList.append(addJob(startDate=current_date, endDate=current_date, data=job, driverData = driver, contents=selectedContents))
                current_date += timedelta(days=1)
                
    driversList = [{'id': driver.driverId, 'title': driver.name} for driver in drivers]
    
    return JsonResponse({'status': True, 'appointments': appointmentsList, 'drivers': driversList})
 