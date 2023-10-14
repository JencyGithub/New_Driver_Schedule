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



# Create your views here.
def leaveReq(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'gearBox/LeaveReq.html', {'leave_requests': leave_requests})

def natureOfLeaves(request):
    nature_of_leaves = NatureOfLeave.objects.all()
    return render(request, 'gearBox/natureOfLeaves.html', {'nature_of_leaves': nature_of_leaves})

def addNatureOfLeave(request):
    data = {
        'reason' : 'Sickness'
    }
    insert = insertIntoTable(tableName='NatureOfLeave',dataSet=data)
    
    return HttpResponse(insert)

    

def natureOfLeavesEdit(request):
    return render(request,'gearBox/NatureOfLeavesForm.html')

def leaveReqForm(request,id=None):
    natureOfLeaves = NatureOfLeave.objects.all()
    params = {
            "natureOfLeaves" : natureOfLeaves
        }
    if id:
        data = LeaveRequest.objects.get(id=id)
        data.start_date = dateConverterFromTableToPageFormate(data.start_date)
        data.end_date = dateConverterFromTableToPageFormate(data.end_date)
        params["data"] = data
        
    return render(request,'gearBox/LeaveReqForm.html',params)
        
@csrf_protect
@api_view(['POST'])
def changeLeaveRequest(request,id=None):
    
    employee = Driver.objects.get(driverId = request.POST.get('driverId'))
    reason = NatureOfLeave.objects.get(id = request.POST.get('Reason'))
    
    data = {
        'employee' : employee,
        'start_date' : request.POST.get('StartDate'),
        'end_date' : request.POST.get('EndDate'),
        'reason' :reason,
    }
    if id == None:
        data['status'] = 'Pending'
        insert = insertIntoTable(tableName='LeaveRequest',dataSet=data)
        messages.success(request,'Adding successfully')
    else:
        data['status'] = request.POST.get('Status')
        update = updateIntoTable(record_id=id,tableName='LeaveRequest',dataSet=data)
        
    return redirect('gearBox:leaveReq')

    