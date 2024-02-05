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
import os, colorama, subprocess
from django.db.models import Q
from django.contrib.auth.hashers import make_password


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
        data = Driver.objects.get(pk = id)   
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
    # Update 
    if id :
        driverObj = Driver.objects.get(pk=id)
        user = User.objects.get(email = driverObj.email)
        if driverObj.name != driverName:
            if driverName in usernames:
                messages.error( request, "Driver Name  already Exist")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                driverObj.name = driverName
                user.username = driverObj.name
            
        if driverObj.email != request.POST.get('email'):
            if request.POST.get('email') in email_addresses:
                messages.error( request, "Email Address already Exist")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                driverObj.email = request.POST.get('email')
                user.email = driverObj.email        
        
        if driverObj.phone != request.POST.get('phone'):
            driverObj.phone = request.POST.get('phone') 
            
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
            DriverObj.phone = request.POST.get('phone') 
            DriverObj.email = request.POST.get('email')
            DriverObj.password = request.POST.get('password')
            
            user_ = User.objects.create(
                username=DriverObj.name,
                email=DriverObj.email,
                password=DriverObj.password,
                is_staff=True,
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

def truckForm(request, id=None):
    clientIds = Client.objects.all()
    rateCards = RateCard.objects.all()
    preStarts = PreStart.objects.all()
    data=connections = None
    count_ = 1
    if id:
        data = AdminTruck.objects.get(pk=id)
        connections = ClientTruckConnection.objects.filter(truckNumber=id).values()
        # return HttpResponse(connections)
        
        for i in connections:
            i['count'] = count_
            count_ += 1
            i['createdBy'] = User.objects.filter(pk=i['createdBy_id']).first().username
            preStartObj =PreStart.objects.filter(pk=i['pre_start_name']).first()
            i['pre_start_name'] = preStartObj.preStartName
            # return HttpResponse(i['pre_start_name'])
            i['startDate'] = dateConverterFromTableToPageFormate(i['startDate'])
            if i['endDate']:
                i['endDate'] = dateConverterFromTableToPageFormate(i['endDate'])
                
        # return HttpResponse(connections)
    params = {
        'clientIds' : clientIds,
        'rateCards' : rateCards,
        'data' : data,
        'connections' : connections,
        'preStarts':preStarts
    }
    return render(request,'GearBox/truck/truckForm.html',params)

@csrf_protect
def truckFormSave(request):
    return redirect('gearBox:truckAxlesFormView')
    
    # return HttpResponse(request.POST.get('truckNo'))
    # dataList = {
    #     'adminTruckNumber' : request.POST.get('truckNo'),
    # }
    # insertIntoTable(tableName='AdminTruck',dataSet=dataList)

    # messages.success(request,'Adding successfully')
    # return redirect('gearBox:truckTable')

def truckAxlesFormView(request):
    return render(request,'GearBox/truck/truckAxlesForm.html')

def truckAxlesFormSave(request):
    return redirect('gearBox:truckSettingFormView')

def  truckSettingFormView(request):
    return render(request,'GearBox/truck/truckSettingForm.html')

def truckSettingFormSave(request):
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
    
    params = {
        'clientIds' : clientIds,
        'rateCards' : rateCards,
        'truckType' : request.POST.get('truckType'),
        'id' : id,
        'preStarts':preStarts
    }
    return render(request,'GearBox/clientTruckConnectionForm.html',params)

@csrf_protect
def truckConnectionSave(request,id):
    adminTruck = AdminTruck.objects.get(id=id)
    rateCard = RateCard.objects.get(pk=request.POST.get('rate_card_name'))
    client = Client.objects.get(pk=request.POST.get('clientId'))
    dataList = {
        'truckNumber' : adminTruck,
        'rate_card_name' : rateCard,
        'clientId' : client,
        'pre_start_name': request.POST.get('pre_start_name'),
        'clientTruckId' : request.POST.get('clientTruckNumber'),
        'truckType' : request.POST.get('truckType'),
        'startDate' : request.POST.get('startDate'),
        'endDate' : request.POST.get('endDate'),
        'createdBy' : request.user
    }

    existingData = ClientTruckConnection.objects.filter(Q(truckNumber = adminTruck,clientId=dataList['clientId'],startDate__gte = dataList['startDate'],startDate__lte = dataList['endDate'])|Q(truckNumber = adminTruck,clientId=dataList['clientId'],endDate__gte = dataList['startDate'],endDate__lte = dataList['endDate'])).first()
    if existingData:
        messages.error( request, "Connection already exist.")
        return redirect(request.META.get('HTTP_REFERER'))
    try:
        oldData = ClientTruckConnection.objects.get(clientId=request.POST.get('clientId'),clientTruckId=request.POST.get('clientTruckNumber'),truckNumber=id)
        if oldData:
            oldData.endDate = getYesterdayDate(request.POST.get('StartDate'))
            oldData.save()
    except:
        pass
    insertIntoTable(tableName='ClientTruckConnection',dataSet=dataList)
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
def getRateCard(request):
    clientId = request.POST.get('clientName')
    clientName = Client.objects.filter(pk = clientId).first()
    rateCardList = RateCard.objects.filter(clientName = clientName).values()
    print(rateCardList)
    return JsonResponse({'status': True, 'rateCard': list(rateCardList)})


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
    data = None
    if id:
        data = Client.objects.get(pk=id)

    params = {
        'data' : data
    }
    return render(request, 'GearBox/clientForm.html', params)

@csrf_protect
def clientChange(request, id=None):
    clientObj = None
    if id:
        clientObj = Client.objects.filter(pk=id).first()
    else:
        clientObj = Client()

    clientObj.name = request.POST.get('name').lower().strip()  
    clientObj.email = request.POST.get('email')
    clientObj.docketGiven = True if request.POST.get('docketGiven') == 'on' else False  
    clientObj.createdBy = request.user 
    clientObj.save()

    
    # dataList =  {
    #     'name' : request.POST.get('name').lower().strip(),
    #     'email' : request.POST.get('email'),
    #     'docketGiven' : True if request.POST.get('docketGiven') == 'on' else False,
    #     'createdBy' : request.user
    # }
    
    # if id:
    #     updateIntoTable(record_id=id,tableName='Client',dataSet=dataList)
    #     messages.success(request,'Updated successfully')
    # else:
    #     insertIntoTable(tableName='Client',dataSet=dataList)
    #     messages.success(request,'Added successfully')

    return redirect('gearBox:clientTable')

def addGroups(request):
    return render(request,'GearBox/groupsForm.html')

def addSubGroups(request):
    return render(request, 'GearBox/subgroupsForm.html')
