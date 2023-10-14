from django.shortcuts import render
from Account_app.models import *
from GearBox_app.models import *
from django.conf import settings
from .models import *
from CRUD import *
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse

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

def addLeaveRequest(request):
    employee = Driver.objects.first()
    reason = NatureOfLeave.objects.first()
    
    data = {
        'employee' : employee,
        'start_date' : '2023-10-13',
        'end_date' : '2023-10-13',
        'reason' :reason
    }
    
    insert = insertIntoTable(tableName='LeaveRequest',dataSet=data)
    return HttpResponse(insert)
    

def natureOfLeavesEdit(request):
    return render(request,'gearBox/NatureOfLeavesEdit.html')

def leaveReqEdit(request):
    return render(request,'gearBox/LeaveReqEdit.html')