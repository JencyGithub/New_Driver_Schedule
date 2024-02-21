from django.shortcuts import render
from Account_app.models import *
from GearBox_app.models import *
from django.conf import settings
from .models import *
from CRUD import *
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.models import User , Group
import os, colorama, subprocess, json
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.core.serializers import serialize
from django.http import FileResponse
import pandas as pd

# Create your views here.
def leaveReq(request):
    leave_requests = LeaveRequest.objects.all().order_by('-status')
    return render(request, 'gearBox/table/LeaveReq.html', {'leave_requests': leave_requests})

def natureOfLeaves(request):
    nature_of_leaves = NatureOfLeave.objects.all()
    return render(request, 'gearBox/table/NatureOfLeaves.html', {'nature_of_leaves': nature_of_leaves})

def natureOfLeavesForm(request,id=None):
    data = None
    if id:
        try:
            data = NatureOfLeave.objects.get(id=id)
        except NatureOfLeave.DoesNotExist:
            raise Http404("NatureOfLeave does not exist")
    return render(request,'gearBox/NatureOfLeavesForm.html',{'data': data}) 

@csrf_protect
@api_view(['POST'])
def changeNatureOfLeaves(request,id=None):
    data = {
        'reason' : request.POST.get('Reason'),
    }
    if id == None:
        insert = insertIntoTable(tableName='NatureOfLeave',dataSet=data)
        messages.success(request,'Adding successfully')
    else:
        update = updateIntoTable(id,tableName='NatureOfLeave',dataSet=data)
        messages.success(request, 'Updating successfully')
    return redirect('gearBox:natureOfLeaves')

def leaveReqForm(request,id=None):
    natureOfLeaves = NatureOfLeave.objects.all()
    drivers = Driver.objects.all()
    params = {
            "natureOfLeaves" : natureOfLeaves,
            "drivers" : drivers,
        }
    if id:
        data = LeaveRequest.objects.get(id=id)
        data.start_date = dateConverterFromTableToPageFormate(data.start_date)
        data.end_date = dateConverterFromTableToPageFormate(data.end_date)
        params["data"] = data
        
    return render(request,'gearBox/LeaveReqForm.html',params)
        
@csrf_protect
def changeLeaveRequest(request,id=None):
    if id == None:
        employee = Driver.objects.get(driverId = request.POST.get('driverId'))
        reason = NatureOfLeave.objects.get(id = request.POST.get('Reason'))
        
        data = {
            'employee' : employee,
            'start_date' : request.POST.get('StartDate'),
            'end_date' : request.POST.get('EndDate'),
            'reason' :reason,
        }
        data['status'] = 'Pending'
        insert = insertIntoTable(tableName='LeaveRequest',dataSet=data)
        messages.success(request,'Adding successfully')
    else:
        requestObj = LeaveRequest.objects.filter(pk=id).first()
        requestObj.status = request.POST.get('status')
        requestObj.comment = request.POST.get('comment')
        requestObj.closedBy = request.user
        requestObj.save()
        messages.success(request,'Updated successfully')        
        
    return redirect('gearBox:leaveReq')


def driversView(request):
    drivers = Driver.objects.all()
    params = {
        'drivers' : drivers
    }
    return render(request,'GearBox/table/driverTable.html',params)

def adminStaffView(request):
    staff = User.objects.exclude(groups__name = "Driver")
    params = {
        'staff' : staff
    }
    return render(request,'GearBox/table/adminStaffTable.html',params)

def adminStaffForm(request, id=None):
    userObj = None
    if id:
        userObj = User.objects.filter(pk=id).first()
    params = {
        'userObj' : userObj
    }
    return  render(request,'GearBox/adminStaffForm.html', params)

@csrf_protect
def adminStaffSave(request, id=None):
    firstName = request.POST.get('firstName')
    lastName = request.POST.get('lastName')
    password = request.POST.get('password')
    email = request.POST.get('email')
    group = request.POST.get('userType')
    isActive = True
    userObj = None
    msg = "Staff created successfully."
    if id:
        userObj = User.objects.filter(pk=id).first()
        isActive = request.POST.get('isActive')
        msg = "Staff updated successfully."
    else:
        existingUser = User.objects.filter(Q(email=email) | Q(username=firstName.lower().strip())).first()
        if existingUser:
            messages.error( request, "This user is already Exist.")
            return redirect(request.META.get('HTTP_REFERER'))
        userObj = User()
        userObj.username=firstName.lower().strip()
        userObj.password=make_password(password) 
        
    userObj.first_name=firstName
    userObj.last_name=lastName
    userObj.email=email
    userObj.is_staff=True 
    userObj.is_active= True if isActive else False 
    userObj.save() 
    
    userObj.groups.clear()
    
    if group != 'Admin':
        groupObj = Group.objects.get(name=group)
        userObj.groups.add(groupObj)
    
    messages.success( request, msg)
    return redirect('gearBox:adminStaffTable')


def driverForm(request, id=None):
    data = None
    if id:
        data = Driver.objects.filter(pk = id).first() 
        data.countryCode = data.phone[:2]  
        data.phone = data.phone[2:]
    params = {
        'data' : data
    }
    return render(request, 'GearBox/driverForm.html',params)


@csrf_protect
def driverFormSave(request, id= None):
    users = User.objects.all()
    drivers = Driver.objects.all()

    usernames = [user.username for user in users]
    email_addresses = [user.email for user in users]
    driver_Id = [driver.driverId for driver in drivers]
    driverName = request.POST.get('name').strip().replace(' ','').lower()
    firstName = request.POST.get('firstName').strip().replace(' ','').lower()
    middleName = request.POST.get('middleName').strip().replace(' ','').lower()
    lastName = request.POST.get('lastName').strip().replace(' ','').lower()

    # Update 
    if id :
        driverObj = Driver.objects.get(pk=id)
        user = User.objects.get(email = driverObj.email)
        if driverObj.name != driverName:
            if driverName in usernames:
                messages.error( request, "Driver Name already Exist")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                driverObj.name = driverName
                driverObj.firstName = firstName
                driverObj.middleName = middleName
                driverObj.lastName = lastName
                user.username = driverObj.name
                user.first_name = driverObj.firstName
                user.last_name = driverObj.LastName
            
        if driverObj.email != request.POST.get('email'):
            if request.POST.get('email') in email_addresses:
                messages.error( request, "Email Address already Exist")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                driverObj.email = request.POST.get('email')
                user.email = driverObj.email        
        
        if driverObj.phone != request.POST.get('phone'):
            driverObj.phone = str(request.POST.get('countryCode')) + str(request.POST.get('phone'))  
            
        user.save()
        driverObj.save()
        messages.success(request,'Updating successfully')
    else:
        if int(request.POST.get('driverId')) in driver_Id :
            messages.error( request, "Driver ID already Exist")
            return redirect(request.META.get('HTTP_REFERER'))
        elif driverName in usernames:
            messages.error( request, "Driver Name  already Exist")
            return redirect(request.META.get('HTTP_REFERER'))
        elif request.POST.get('email') in email_addresses:
            messages.error( request, "Email Address already Exist")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            DriverObj = Driver()
            DriverObj.driverId = int(request.POST.get('driverId'))
            DriverObj.name = driverName
            DriverObj.phone = str(request.POST.get('countryCode')) + str(request.POST.get('phone')) 
            DriverObj.email = request.POST.get('email')
            DriverObj.password = request.POST.get('password')
            DriverObj.firstName = firstName
            DriverObj.middleName = middleName
            DriverObj.lastName = lastName
            
            user_ = User.objects.create(
                username=DriverObj.name,
                email=DriverObj.email,
                password=DriverObj.password,
                is_staff=True,
                first_name = DriverObj.firstName,
                last_name = DriverObj.lastName,
            )  
            group = Group.objects.get(name='Driver')
            user_.groups.add(group)
            
            user_.set_password(DriverObj.password)
            user_.save()
            DriverObj.save()
            messages.success(request,'Driver Entry successfully')
            
            
            with open("scripts/addPastTripForMissingDriver.txt", 'w') as f:
                f.write(driverName)
            # colorama.AnsiToWin32.stream = None
            # os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
            # cmd = ["python", "manage.py", "runscript", 'addPastTripForMissingDriver','--continue-on-error']
            # subprocess.run(cmd)
            colorama.AnsiToWin32.stream = None
            os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
            cmd = ["python", "manage.py", "runscript", 'addPastTripForMissingDriver','--continue-on-error']
            subprocess.Popen(cmd, stdout=subprocess.PIPE)
            
            

    return redirect('gearBox:driversTable')


# ````````````````````````````````````````

# Compliance Section 

# ````````````````````````````````````````````````

def medicalsTable(request):
    return render(request,'GearBox/Compliance/medicalsTable.html')

def trainingTable(request):
    return render(request, 'GearBox/Compliance/trainingTable.html')


# ````````````````````````````````````````

# Safety

# ````````````````````````````````````````````````


def vehicleAccidentsTable(request):
    return render(request, 'GearBox/Safety/vehicleAccidentsTable.html')

def equipmentIssueTable(request):
    return render(request, 'GearBox/Safety/equipmentIssueTable.html')

# ````````````````````````````````````````

# Reminder

# ````````````````````````````````````````````````

def reminderTable(request):
    return render(request, 'GearBox/reminderTable.html')

# ````````````````````````````````````````

# Truck Section 

# ````````````````````````````````````````````````

def truckTable(request):
    adminTruck = AdminTruck.objects.all()
    params = {
        'adminTrucks' : adminTruck
    }
    return render(request , 'GearBox/truck/table/truckTable.html',params)

def truckForm(request, id=None, viewOnly= None):
    truckInformationCustomObj = None
    clientIds = Client.objects.all()
    clientOfcObj = ClientOffice.objects.all()
    rateCards = RateCard.objects.all()
    preStarts = PreStart.objects.all()
    adminTruckObj=truckInformationObj=connections = None
    curDate = getCurrentDateTimeObj().date()
    truckInformationCustomObj = TruckInformationCustom.objects.filter(active=True)

    count_ = 1
    if id:
        adminTruckObj = AdminTruck.objects.filter(pk=id).first()
        truckInformationObj = adminTruckObj.truckInformation
        connections = ClientTruckConnection.objects.filter(truckNumber=id).values()
        
        for i in connections:
            i['count'] = count_
            if i['startDate'] <= curDate and i['endDate'] > curDate:
                i['status'] = True
            count_ += 1
            i['createdBy'] = User.objects.filter(pk=i['createdBy_id']).first().username
            preStartObj =PreStart.objects.filter(pk=i['pre_start_name']).first()
            
            if preStartObj:
                i['pre_start_name'] = preStartObj.preStartName
            i['startDate'] = dateConverterFromTableToPageFormate(i['startDate'])
            if i['endDate']:
                i['endDate'] = dateConverterFromTableToPageFormate(i['endDate'])

        for i in range(1, len(truckInformationCustomObj)+1):
            field_str = 'customFieldValue' + str(i)
            try:
                value = getattr(truckInformationObj, field_str)
                truckInformationCustomObj[i-1].customFieldValue = value
                print(truckInformationCustomObj[i-1].customFieldValue)
            except :
                pass
                
    params = {
        'clientIds' : clientIds,
        'rateCards' : rateCards,
        'adminTruckObj' : adminTruckObj,
        'truckInformationObj':truckInformationObj,
        'connections' : connections,
        'preStarts':preStarts,
        'clientOfcObj':clientOfcObj,
        'truckInformationCustomObj':truckInformationCustomObj,
        'viewOnly':viewOnly,
        'groups' : TruckGroup.objects.all()
    }
    return render(request,'GearBox/truck/truckForm.html',params)

@csrf_protect
def truckFormSave(request,truckId=None):
    adminTruckObj = AdminTruck()
    truckInformationObj = TruckInformation()
    viewOnly = 1 if request.POST.get('viewOnly') != 'None' else 0
    truckNo = request.POST.get('truckNo')
    truckObj = AdminTruck.objects.filter(adminTruckNumber = truckNo).first()
    if truckObj and truckId is None:
        messages.error(request,'Truck number already exist')
        return redirect(request.META.get('HTTP_REFERER'))
    elif not viewOnly:
        if truckId:
            adminTruckObj = AdminTruck.objects.filter(pk=truckId).first()
            truckInformationObj = adminTruckObj.truckInformation
            

        adminTruckObj.adminTruckNumber = truckNo
        adminTruckObj.createdBy = request.user
        adminTruckObj.truckActive = True    
        
        truckInformationObj.fleet = truckNo
        truckInformationObj.groups = request.POST.get('groups')
        truckInformationObj.subGroups = request.POST.get('subGroups')
        truckInformationObj.vehicleType = request.POST.get('vehicleType')
        truckInformationObj.serviceGroup = request.POST.get('serviceGroup')

        truckImg1 = request.FILES.get('truckImg1')
        truckImg2 = request.FILES.get('truckImg2')
        truckImg3 = request.FILES.get('truckImg3')
        if truckImg1:
            truckInformationObj.truckImg1 = truckFileSave(truckImg1)
        if truckImg2:
            truckInformationObj.truckImg2 = truckFileSave(truckImg2)
        if truckImg3:
            truckInformationObj.truckImg3 = truckFileSave(truckImg3)
            
        if request.POST.get('customFieldLabel1') != None:
            truckInformationCustomObj = TruckInformationCustom.objects.filter(pk=request.POST.get('customFieldLabel1')).first()
            truckInformationObj.customFieldLabel1 = truckInformationCustomObj.customFieldLabel
        truckInformationObj.customFieldValue1 = request.POST.get('customFieldValue1')
        # return HttpResponse(request.POST.get('customFieldLabel1'))
            
        if request.POST.get('customFieldLabel2') != None:
            truckInformationCustomObj = TruckInformationCustom.objects.filter(pk=request.POST.get('customFieldLabel2')).first()
            truckInformationObj.customFieldLabel2 = truckInformationCustomObj.customFieldLabel
        truckInformationObj.customFieldValue2 = request.POST.get('customFieldValue2')
            
        if request.POST.get('customFieldLabel3') != None:
            truckInformationCustomObj = TruckInformationCustom.objects.filter(pk=request.POST.get('customFieldLabel3')).first()
            truckInformationObj.customFieldLabel3 = truckInformationCustomObj.customFieldLabel
        truckInformationObj.customFieldValue3 = request.POST.get('customFieldValue3')
            
        if request.POST.get('customFieldLabel4') != None:
            truckInformationCustomObj = TruckInformationCustom.objects.filter(pk=request.POST.get('customFieldLabel4')).first()
            truckInformationObj.customFieldLabel4 = truckInformationCustomObj.customFieldLabel
        truckInformationObj.customFieldValue4 = request.POST.get('customFieldValue4')
            
        if request.POST.get('customFieldLabel5') != None:
            truckInformationCustomObj = TruckInformationCustom.objects.filter(pk=request.POST.get('customFieldLabel5')).first()
            truckInformationObj.customFieldLabel5 = truckInformationCustomObj.customFieldLabel
        truckInformationObj.customFieldValue5 = request.POST.get('customFieldValue5')
            
        if request.POST.get('customFieldLabel6') != None:
            truckInformationCustomObj = TruckInformationCustom.objects.filter(pk=request.POST.get('customFieldLabel6')).first()
            truckInformationObj.customFieldLabel6 = truckInformationCustomObj.customFieldLabel
        truckInformationObj.customFieldValue6 = request.POST.get('customFieldValue6')
            
            
        # for i in 
        # truckInformationObj.customFuelCard = request.POST.get('customFuelCard')
        # truckInformationObj.customFuelOldFleetNumber = request.POST.get('customOldFeetNumber')
        # truckInformationObj.customOldRego = request.POST.get('customOldRego')
        # truckInformationObj.customRegisteredOwner = request.POST.get('customRegOwner')
        # truckInformationObj.customRoadsideAssistance = request.POST.get('customRoadsideAssistance')
        # truckInformationObj.customPDDNumber = request.POST.get('customPdd')
        
        truckInformationObj.informationMake = request.POST.get('informationMake')
        truckInformationObj.informationModel = request.POST.get('informationModel')
        truckInformationObj.informationConfiguration = request.POST.get('informationConfiguration')
        truckInformationObj.informationChassis = request.POST.get('informationChassis')
        truckInformationObj.informationBuildYear = request.POST.get('informationBuildYear')
        truckInformationObj.informationIcon = request.POST.get('informationIcon')
        
        truckInformationObj.registered = False if request.POST.get('registered')  else True
        # return HttpResponse(truckInformationObj.registered)
        if truckInformationObj.registered:
            truckInformationObj.registration = request.POST.get('registration')
            truckInformationObj.registrationCode = request.POST.get('registrationCode')
            truckInformationObj.registrationState = request.POST.get('registrationState')
            truckInformationObj.registrationDueDate = request.POST.get('registrationDueDate')
            truckInformationObj.registrationInterval = request.POST.get('registrationInterval')
        truckInformationObj.powered = True if request.POST.get('powered') =='on' else False
        truckInformationObj.engine = request.POST.get('engine')
        truckInformationObj.engineMake = request.POST.get('engineMake')
        truckInformationObj.engineModel = request.POST.get('engineModel')
        truckInformationObj.engineCapacity = request.POST.get('engineCapacity')
        truckInformationObj.engineGearBox = request.POST.get('engineGearbox')
        truckInformationObj.save()
        
        adminTruckObj.truckInformation = truckInformationObj
        adminTruckObj.save()
        
        return redirect('gearBox:truckAxlesFormView',truckId=adminTruckObj.id,viewOnly=viewOnly)
    return redirect('gearBox:truckAxlesFormView',truckId=truckId,viewOnly=viewOnly)


def truckAxlesFormView(request,truckId,viewOnly):
    truckAxlesObj = None
    truckAxlesObj_serialized = None
    adminTruckObj = AdminTruck.objects.filter(pk=truckId).first()
    if adminTruckObj.truckAxles:
        truckAxlesObj = adminTruckObj.truckAxles
        truckAxlesObj_serialized = serialize('json', [truckAxlesObj])
        
    params={
    'adminTruckObj':adminTruckObj,
    'truckAxlesObj':truckAxlesObj,
    'viewOnly':viewOnly,
    'truckAxlesObj_serialized':truckAxlesObj_serialized
    }
    
    return render(request,'GearBox/truck/truckAxlesForm.html',params)

def truckAxlesFormSave(request,truckId):
    viewOnly = request.POST.get('viewOnly') 
    if viewOnly == '1':
        return redirect('gearBox:truckSettingFormView',truckId=truckId ,viewOnly=viewOnly)

    adminTruckObj = AdminTruck.objects.filter(pk=truckId).first()
    check = adminTruckObj.truckAxles
    if adminTruckObj.truckAxles:
        truckAxlesObj = adminTruckObj.truckAxles 
    else:
        truckAxlesObj = Axles()
    truckAxlesObj.vehicle_axle1 = request.POST.get('vehicle_axle1')
    truckAxlesObj.vehicle_axle2 = request.POST.get('vehicle_axle2')
    truckAxlesObj.vehicle_axle3 = request.POST.get('vehicle_axle3')
    truckAxlesObj.vehicle_axle4 = request.POST.get('vehicle_axle4')
    truckAxlesObj.vehicle_axle5 = request.POST.get('vehicle_axle5')
    truckAxlesObj.vehicle_axle6 = request.POST.get('vehicle_axle6')
    truckAxlesObj.vehicle_axle7 = request.POST.get('vehicle_axle7')
    truckAxlesObj.vehicle_axle8 = request.POST.get('vehicle_axle8')
    truckAxlesObj.save()
    adminTruckObj = AdminTruck.objects.filter(pk=truckId).first()
    adminTruckObj.truckAxles = truckAxlesObj
    adminTruckObj.save()
    # where first ime store axle value  and then update vehicle detail page with new data
    if check is None:
        return redirect(request.META.get('HTTP_REFERER'))
    else:
    # messages.success(request, 'Update successfully' if adminTruckObj.truckAxles else 'Adding successfully')

        return redirect('gearBox:truckSettingFormView',truckId=truckId ,viewOnly=viewOnly)

def axleInformationSave(request,axleId,inputNumber):
    truckAxleObj = Axles.objects.filter(pk=axleId).first()
    setattr(truckAxleObj, 'axle_make' + str(inputNumber), request.POST.get('axle_make' + str(inputNumber)))
    setattr(truckAxleObj, 'axle_rims' + str(inputNumber), request.POST.get('axle_rims' + str(inputNumber)))
    setattr(truckAxleObj, 'axle_tyre_size' + str(inputNumber), request.POST.get('axle_tyre_size' + str(inputNumber)))
    setattr(truckAxleObj, 'axle_suspensions' + str(inputNumber), request.POST.get('axle_suspensions' + str(inputNumber)))
    setattr(truckAxleObj, 'axle_brakes' + str(inputNumber), request.POST.get('axle_brakes' + str(inputNumber)))
    setattr(truckAxleObj, 'axle_slack_adjusters' + str(inputNumber), request.POST.get('axle_slack_adjusters' + str(inputNumber)))
    setattr(truckAxleObj, 'axle_differential' + str(inputNumber), request.POST.get('axle_differential' + str(inputNumber)))
    truckAxleObj.save()
    return redirect(request.META.get('HTTP_REFERER'))


def  truckSettingFormView(request,truckId,viewOnly):
    adminTruckObj = AdminTruck.objects.filter(pk=truckId).first()
    params={
        'adminTruckObj':adminTruckObj,
        'viewOnly':viewOnly,
    }
    return render(request,'GearBox/truck/truckSettingForm.html',params)

def truckSettingFormSave(request):
    # truckSettingObj.fuelType = request.POST.get('fuelType')
    # truckSettingObj.FuelCreditCategory = request.POST.get('FuelCreditCategory')
    # truckSettingObj.adbluePercent = request.POST.get('adbluePercent')
    # truckSettingObj.kilometresOffset = request.POST.get('kilometresOffset')
    # truckSettingObj.hoursOffset = request.POST.get('hoursOffset')
    # truckSettingObj.prestartChecklist = request.POST.get('prestartChecklist')
    # truckSettingObj.trailers = request.POST.get('trailers')
    # truckSettingObj.GCM = request.POST.get('GCM')
    # truckSettingObj.GVM = request.POST.get('GVM')
    # truckSettingObj.TARE = request.POST.get('TARE')
    # truckSettingObj.ATM = request.POST.get('ATM')
    # truckSettingObj.Length = request.POST.get('Length')
    # truckSettingObj.Height = request.POST.get('Height')
    # truckSettingObj.Width = request.POST.get('Width')
    # truckSettingObj.Volume = request.POST.get('Volume')
    # truckSettingObj.Pallets = request.POST.get('Pallets')
    # truckSettingObj.spareField7 = request.POST.get('spareField7')
    # truckSettingObj.spareField8 = request.POST.get('spareField8')
    # truckSettingObj.spareField9 = request.POST.get('spareField9')
    # truckSettingObj.spareField10 = request.POST.get('spareField10')
    # truckSettingObj.spareField11 = request.POST.get('spareField11')
    # truckSettingObj.spareField12 = request.POST.get('spareField12')
    # truckSettingObj.spareField13 = request.POST.get('spareField13')
    # truckSettingObj.spareField14 = request.POST.get('spareField14')
    # truckSettingObj.spareField15 = request.POST.get('spareField15')
    # truckSettingObj.spareField16 = request.POST.get('spareField16')
    # truckSettingObj.spareField17 = request.POST.get('spareField17')
    # truckSettingObj.spareField18 = request.POST.get('spareField18')
    # truckSettingObj.spareField19 = request.POST.get('spareField19')
    # truckSettingObj.spareField20 = request.POST.get('spareField20')
    # truckSettingObj.description = request.POST.get('description')
    return redirect('gearBox:truckRemindersFormView')

def  truckRemindersFormView(request):
    return render(request,'GearBox/truck/truckRemindersForm.html')

def truckRemindersFormSave(request):
    return redirect('gearBox:truckPartsFormView')

def  truckPartsFormView(request):
    return render(request,'GearBox/truck/truckPartsForm.html')

def truckPartsFormSave(request):
    return redirect('gearBox:truckHistoryFormView')

def  truckHistoryFormView(request):
    return render(request,'GearBox/truck/truckHistoryForm.html')

def truckHistoryFormSave(request):
    return redirect('gearBox:truckOdometerFormView')

def  truckOdometerFormView(request):
    return render(request,'GearBox/truck/truckOdometerForm.html')

def truckOdometerFormSave(request):
    return redirect('gearBox:truckComplianceFormView')

def  truckComplianceFormView(request):
    return render(request,'GearBox/truck/truckComplianceForm.html')

def truckComplianceFormSave(request):
    return redirect('gearBox:truckDocumentsFormView')

def  truckDocumentsFormView(request):
    return render(request,'GearBox/truck/truckDocumentsForm.html')

def truckDocumentsFormSave(request):
    return HttpResponse('Stop')
    # return redirect('gearBox:truckDocumentsFormView')


def truckConnectionForm(request, id):
    clientIds = Client.objects.all()
    rateCards = RateCard.objects.all()
    preStarts = PreStart.objects.all()
    # basePlantObj = BasePlant.objects.filter(clientDepot = True)
    params = {
        'clientIds' : clientIds,
        'rateCards' : rateCards,
        'truckType' : request.POST.get('truckType'),
        'id' : id,
        # 'basePlantObj' : basePlantObj,
        'preStarts':preStarts
    }
    # return HttpResponse(basePlantObj)
    return render(request,'GearBox/clientTruckConnectionForm.html',params)

@csrf_protect
def truckConnectionSave(request,id):
    adminTruck = AdminTruck.objects.get(id=id)
    rateCard = RateCard.objects.get(pk=request.POST.get('rate_card_name'))
    client = Client.objects.get(pk=request.POST.get('clientId'))
    clientOfcObj = ClientOffice.objects.filter(pk=request.POST.get('clientOfc')).first()
    dataList = {
        'truckNumber' : adminTruck,
        'rate_card_name' : rateCard,
        'clientId' : client,
        'pre_start_name': request.POST.get('pre_start_name'),
        'clientTruckId' : request.POST.get('clientTruckNumber'),
        'truckType' : request.POST.get('truckType'),
        'startDate' : request.POST.get('startDate'),
        'endDate' : request.POST.get('endDate'),
        'clientOfc': clientOfcObj,
        'neverEnding':True if request.POST.get('neverEnding') == 'on' else False,
        'createdBy' : request.user
    }

    existingData = ClientTruckConnection.objects.filter(Q(truckNumber = adminTruck,clientId=dataList['clientId'],startDate__gte = dataList['startDate'],startDate__lte = dataList['endDate'])|Q(truckNumber = adminTruck,clientId=dataList['clientId'],endDate__gte = dataList['startDate'],endDate__lte = dataList['endDate'])).first()
    if existingData:
        messages.error(request, "Connection already exist.")
        return redirect(request.META.get('HTTP_REFERER'))
    try:
        oldData = ClientTruckConnection.objects.get(clientId=request.POST.get('clientId'),clientTruckId=request.POST.get('clientTruckNumber'),truckNumber=id)
        if oldData:
            oldData.endDate = getYesterdayDate(request.POST.get('StartDate'))
            oldData.save()
    except:
        pass
    
    data = insertIntoTable(tableName='ClientTruckConnection',dataSet=dataList)
    with open("scripts/addPastTripForMissingTruckNo.txt", 'w') as f:
        f.write(str(dataList['truckNumber']))

    colorama.AnsiToWin32.stream = None
    os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
    cmd = ["python", "manage.py", "runscript", 'addPastTripForMissingTruckNo','--continue-on-error']
    subprocess.Popen(cmd, stdout=subprocess.PIPE)
    messages.success(request,'Truck Connection Add Successfully')
    return redirect('gearBox:truckTable')

    # Document
@csrf_protect
def truckConnectionDeactivate(request):
    print('here')
    status = False
    current_date = getCurrentDateTimeObj().date()
    truckConnectionId = request.POST.get('connectionId_')
    adminTruckObj = AdminTruck.objects.filter(pk=truckConnectionId).first()
    existing_appointments = AppointmentTruck.objects.filter(
        truckNo=adminTruckObj,
        appointmentId__startDate__lte=current_date,
        appointmentId__endDate__gte=current_date
    )
    if not existing_appointments:
        status = True
        clientTruckConnectionObj = ClientTruckConnection.objects.filter(pk=truckConnectionId).first()
        clientTruckConnectionObj.endDate = current_date
        clientTruckConnectionObj.save()
        print(existing_appointments)
    return JsonResponse({'status': status})

@csrf_protect
def getRateCard(request):
    clientOfficeId = request.POST.get('clientOffice')
    clientOfficeObj = ClientOffice.objects.filter(pk = clientOfficeId).first()
    rateCardList = RateCard.objects.filter(clientOfc = clientOfficeObj).values()
    print(rateCardList)
    return JsonResponse({'status': True, 'rateCard': list(rateCardList)})


@csrf_protect
def getClientOffice(request):
    clientId = request.POST.get('clientName')
    clientObj = Client.objects.filter(pk = clientId).first()
    clientOfficeObj = ClientOffice.objects.filter(clientId = clientObj).values()
    return JsonResponse({'status': True, 'clientOfficeObj': list(clientOfficeObj)})
    
# Settings Form 

def settingsForm(request):
    return render(request,'GearBox/truck/settingsForm.html')

# Compliance Form 

def complianceForm(request):
    return render(request,'GearBox/truck/complianceForm.html')

# ```````````````````````````````````
# Client 
# ```````````````````````````````````

def clientTable(request):
    clients = Client.objects.all()
    params = {
        'clients' : clients
    }
    return render(request,'GearBox/table/client.html',params)

def clientForm(request, id=None):
    data, ofcObjs = None, None
    if id:
        data = Client.objects.filter(pk=id).first()
        ofcObjs = ClientOffice.objects.filter(clientId=data)

    params = {
        'data' : data,
        'ofcObjs' : ofcObjs
    }
    return render(request, 'GearBox/clientForm.html', params)

@csrf_protect
def clientChange(request, id=None):
    clientObj = Client()
    
    if id:
        clientObj = Client.objects.filter(pk=id).first()

    clientObj.name = request.POST.get('name').lower().strip()  
    clientObj.email = request.POST.get('email')
    clientObj.docketGiven = True if request.POST.get('docketGiven') == 'on' else False  
    clientObj.createdBy = request.user 
    clientObj.save()
    
    clientOfcObj = ClientOffice() 
    clientOfcObj.clientId = clientObj
    clientOfcObj.locationType = request.POST.get('addType')
    clientOfcObj.description = request.POST.get('addDescription')
    clientOfcObj.address1 = request.POST.get('address1')
    clientOfcObj.address2 =request.POST.get('address2')
    clientOfcObj.personName = request.POST.get('personName')   
    clientOfcObj.city = request.POST.get('addCity')
    clientOfcObj.state = request.POST.get('addState')
    clientOfcObj.country = request.POST.get('addCountry') 
    clientOfcObj.postalCode =  request.POST.get('addPostalCode')
    clientOfcObj.primaryContact = str(request.POST.get('countryCode')) + str(request.POST.get('primaryContact')) 
    clientOfcObj.alternativeContact = request.POST.get('alternateContact') if request.POST.get('alternateContact') else None
    clientOfcObj.save()

    return redirect('gearBox:clientTable')

# def addGroups(request):
#     return render(request,'GearBox/groupsForm.html')

@csrf_protect
@api_view(['POST'])
def clientOfcView(request): 
    ofcId = request.POST.get('ofcId')
    ofcObj = ClientOffice.objects.filter(pk=ofcId).values().first()
    ofcObj['countryCode'] = str(ofcObj['primaryContact'])[:-10]
    ofcObj['primaryContact'] = str(ofcObj['primaryContact'])[-10:]
    
    return JsonResponse({ 'status': True, 'ofcObj' : ofcObj})
    
@csrf_protect
def clientOfcEditSave(request, id=None, clientId=None):
    clientOfcObj = ClientOffice()
    if id:
        clientOfcObj = ClientOffice.objects.filter(pk=id).first()
        
    if clientId:
        clientOfcObj.clientId = Client.objects.filter(pk=clientId).first()

    clientOfcObj.locationType = request.POST.get('modalAddType')
    clientOfcObj.description = request.POST.get('modalAddDescription')
    clientOfcObj.address1 = request.POST.get('modalAddress1')
    clientOfcObj.address2 =request.POST.get('modalAddress2')
    clientOfcObj.personName = request.POST.get('modalPersonName')   
    clientOfcObj.city = request.POST.get('modalAddCity')
    clientOfcObj.state = request.POST.get('modalAddState')
    clientOfcObj.country = request.POST.get('modalAddCountry') 
    clientOfcObj.postalCode =  request.POST.get('modalAddPostalCode')
    clientOfcObj.primaryContact = str(request.POST.get('modalCountryCode')) + str(request.POST.get('modalPrimaryContact')) 
    clientOfcObj.alternativeContact = request.POST.get('modalAlternateContact') if request.POST.get('modalAlternateContact') else None
    clientOfcObj.save()

    return redirect(request.META.get('HTTP_REFERER'))

def groupsView(request):
    truckGroupObj = TruckGroup.objects.all()
    params = {
        'truckGroupObj':truckGroupObj
    }
    return render(request,'GearBox/groupsForm.html',params)


@csrf_protect
def addGroupsSave(request , id= None):
    groupName = request.POST.get('groupName')
    truckGroupObj = TruckGroup.objects.filter(pk=id).first()
    existingTruckGroup = TruckGroup.objects.filter(name=groupName).first()
    if existingTruckGroup:
        messages.error(request, 'This Group  Already Exists ')
        return redirect(request.META.get('HTTP_REFERER'))
    if not truckGroupObj:
        truckGroupObj = TruckGroup()
    truckGroupObj.name=groupName
    truckGroupObj.save()
    messages.success(request, 'Add Successfully' if not truckGroupObj else 'Update Successfully')
    return redirect(request.META.get('HTTP_REFERER'))

def subGroupForm(request):
    truckGroupObj = TruckGroup.objects.all()
    truckSubGroupObj = TruckSubGroup.objects.all()
    params = {
        'truckGroupObj':truckGroupObj,
        'truckSubGroupObj':truckSubGroupObj,
    }
    return render(request, 'GearBox/subgroupsForm.html',params)

@csrf_protect
def subGroupSave(request , id=None):
    truckGroupObj = TruckGroup.objects.all()
    truckSubGroupObj = TruckSubGroup.objects.filter(pk=id).first()
    truckGroupObj = TruckGroup.objects.filter(pk=request.POST.get('groups')).first()
    existingTruckSubGroup = TruckSubGroup.objects.filter(name = request.POST.get('subGroups')  , truckGroup =truckGroupObj).first()
    if existingTruckSubGroup:
        messages.error(request, 'This Group  Sub Group Already Exists ')
        return redirect(request.META.get('HTTP_REFERER'))
    if not truckSubGroupObj:
        truckSubGroupObj = TruckSubGroup()
    truckSubGroupObj.truckGroup  =  truckGroupObj
    truckSubGroupObj.name  = request.POST.get('subGroups') 
    truckSubGroupObj.save()
    
    params = {
        'truckGroupObj':truckGroupObj
    }
    messages.success(request, 'Add Successfully' if not truckSubGroupObj else 'Update Successfully')
    return redirect(request.META.get('HTTP_REFERER'))


def fleetSettings(request):
    truckInformationCustomObj = TruckInformationCustom.objects.all()
    addStatus = False
    if TruckInformationCustom.objects.all().count() >= 6:
        print(TruckInformationCustom.objects.all().count())
        addStatus = True
        
    params = {
        'addStatus':addStatus,
        'truckInformationCustomObj':truckInformationCustomObj,
    }
    return render(request, 'GearBox/fleetSettings.html', params)

@csrf_protect
def fleetCustomInformationSave(request, id = None):
    requiredCheck = request.POST.get('requiredCheck')
    requiredField = request.POST.get('requiredField')
    requiredFieldValue = request.POST.getlist('requiredFieldValue')
    
    # Load the JSON data from a file
    with open('static/Account/fleetInformation.json', 'r') as file:
        data = json.load(file)

    inputFields = data["CUSTOM-INFORMATION"]["input-fields"]
    selectFields = data["CUSTOM-INFORMATION"]["select-fields"]    
    fieldName = "customFieldValue" + str(TruckInformationCustom.objects.all().count() + 1)
    
    if requiredCheck == "required":
        data["CUSTOM-INFORMATION"]["All"].append(fieldName)
    else:        
        if requiredField in inputFields:
            data["CUSTOM-INFORMATION"]["input-fields"][requiredField].append(fieldName)
        elif requiredField in selectFields:
            for i in range(len(requiredFieldValue)):
                data["CUSTOM-INFORMATION"]["select-fields"][requiredField][requiredFieldValue[i]].append(fieldName)
            
    with open('static/Account/fleetInformation.json', 'w') as file:
        json.dump(data, file, indent=4)
    
    if not id:
        truckInformationCustomObj = TruckInformationCustom()
        truckInformationCustomObj.customFieldLabel = request.POST.get('customFieldLabel')
    else:
        truckInformationCustomObj = TruckInformationCustom.objects.filter(pk=id).first()
    truckInformationCustomObj.active = True if request.POST.get('active') else False 
    truckInformationCustomObj.save()
    messages.success(request, 'Custom Information update Successfully' if id else 'Custom Information added Successfully' )
    return redirect('gearBox:fleetSettings')

def truckSampleCsv(request):
    existing_custom_field = []
    truck_information_custom_list = []
    custom_column_name = []
    data = pd.read_excel('static/Account/sampleTruckEntry.xlsx')
    build_date_index = data.columns.get_loc('Build Date')
    existing_custom_field = data.columns[build_date_index + 1: build_date_index + 7].tolist()

    truck_information_custom_objects = TruckInformationCustom.objects.all()

    for obj in truck_information_custom_objects:    
        truck_information_custom_list.append(obj.customFieldLabel)
        
    custom_column_name = truck_information_custom_list[0:]
    length_ = len(custom_column_name)
    custom_column_name +=existing_custom_field[length_:]
    
    for i in range(len(custom_column_name)):
        data.rename(columns={'Custom_Field_'+str(i+1): custom_column_name[i]}, inplace=True)

    data.to_excel('static/Account/sampleTruckEntry - Copy.xlsx', index=False)

    return FileResponse(open(f'static/Account/sampleTruckEntry - Copy.xlsx', 'rb'), as_attachment=True)

def bulkTruckEntryForm(request):
    truckEntryErrorObj = TruckEntryError.objects.all()
    params = {
        'truckEntryErrorObj':truckEntryErrorObj
    }
    return render(request, 'GearBox/truck/bulkTruckEntryForm.html',params)

@csrf_protect
def uploadBulkData(request):
    truck_csv_file = request.FILES.get('truckEntryFile')
    if not truck_csv_file:
        messages.warning(request,'Invalid Request')
        return redirect(request.META.get('HTTP_REFERER'))
    try:
        time = (str(timezone.now())).replace(':', '').replace(
            '-', '').replace(' ', '').split('.')
        time = time[0]
        newFileName = time + "@_!" + str(truck_csv_file.name)

        location = 'static/Account/TruckEntry'
        lfs = FileSystemStorage(location=location)
        lfs.save(newFileName, truck_csv_file)
        with open("Truck_entry_file.txt", 'w') as f:
            f.write(newFileName+','+str(request.user))
            f.close()
        colorama.AnsiToWin32.stream = None
        os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
        cmd = ["python", "manage.py", "runscript", 'TruckCsvToModel','--continue-on-error']
        subprocess.Popen(cmd, stdout=subprocess.PIPE)
        messages.success(
            request, "Please wait 5 minutes. The data conversion process continues")
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")