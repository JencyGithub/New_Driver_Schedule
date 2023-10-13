from django.shortcuts import render
from Account_app.models import *
from GearBox_app.models import *
from django.conf import settings
from .models import *

# Create your views here.
def leaveReq(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'gearBox/LeaveReq.html', {'leave_requests': leave_requests})

def natureOfLeaves(request):
    nature_of_leaves = NatureOfLeave.objects.all()
    return render(request, 'gearBox/natureOfLeaves.html', {'nature_of_leaves': nature_of_leaves})

def natureOfLeavesEdit(request):
    return render(request,'gearBox/NatureOfLeavesEdit.html')

def leaveReqEdit(request):
    return render(request,'gearBox/LeaveReqEdit.html')