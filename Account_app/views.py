from django.shortcuts import render,redirect
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import shutil, os,tabula, requests, colorama, subprocess
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib import messages
from Account_app.models import *
from GearBox_app.models import *


def index(request):
    return render(request, 'Account/dashboard.html')

def getForm1(request):
    params = {}
    if request.user.is_authenticated:
        user_email = request.user.email
        client_names = Client.objects.values_list('name', flat=True).distinct()
        admin_truck_no = AdminTruck.objects.values_list(
            'adminTruckNumber', flat=True).distinct()
        client_truck_no = ClientTruckConnection.objects.values_list(
            'clientTruckId', flat=True).distinct()
        basePlant = BasePlant.objects.values_list(
            'basePlant', flat=True).distinct()
        params = {
            'client_ids': client_names,
            'admin_truck_no': admin_truck_no,
            'client_truck_no': client_truck_no,
            'basePlants': basePlant,
        }
        try:
            Driver_  = Driver.objects.get(email=user_email)
            driver_id = str(Driver_.driverId) + '-' + str(Driver_.name)   
            params['driver_ids'] = driver_id
            params['drivers'] = None
            DriverTruckNum = ClientTruckConnection.objects.get(driverId = Driver_.driverId)
            params['DriverTruckNum'] = str(DriverTruckNum.clientTruckId) + '-' + str(DriverTruckNum.truckNumber)
            params['client_names'] = str(DriverTruckNum.clientId.name)


        except Exception as e:
            print(e)
            params['driver_ids'] = None
            drivers = Driver.objects.all()
            params['drivers'] = drivers
            params['DriverTruckNum'] = None
            params['client_names'] = None
            

        return render(request, 'Trip_details/form1.html', params)

    else:
        return redirect('login')
    
    # return render(request, 'Trip_details/Form1.html')

def getForm2(request):
    return render(request, 'Trip_details/Form2.html')


def rcti(request):
    return render(request , 'Account/rctiForm.html')
    
@csrf_protect
def rctiSave(request):
    invoiceFile = request.FILES.get('RctiFile')
    save_data = request.POST.get('save')
    if not invoiceFile:
        return HttpResponse("No file uploaded")
    try:
        time = (str(timezone.now())).replace(':', '').replace('-', '').replace(' ', '').split('.')
        time = time[0]
        newFileName = time + "@_!" + str(invoiceFile.name)
        location = 'static/Account/RCTI/tempRCTIInvoice'

        lfs = FileSystemStorage(location=location)
        lfs.save(newFileName, invoiceFile)

        cmd = ["python","Account_app/utils.py", newFileName]
        subprocess.Popen(cmd,stdout=subprocess.PIPE)  
        # return HttpResponse('work')
        if save_data == '1':
            colorama.AnsiToWin32.stream = None
            os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"      
            cmd = ["python","manage.py", "runscript",'csvToModel.py']
            subprocess.Popen(cmd,stdout=subprocess.PIPE)        
        messages.success(request, "Please wait 5 minutes. The data conversion process continues")
        return redirect('/')
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    
def driverEntry(request):
    return render(request , 'Account/driverEntryForm.html')

@csrf_protect
def driverEntrySave(request):
    Driver_csv_file = request.FILES.get('driverEntryFile')
    if not Driver_csv_file:
        return HttpResponse("No file uploaded")
    try:
        time = (str(timezone.now())).replace(':', '').replace('-', '').replace(' ', '').split('.')
        time = time[0]
        newFileName = time + "@_!" + str(Driver_csv_file.name)
        location = 'static/Account/DriverEntry'

        lfs = FileSystemStorage(location=location)
        lfs.save(newFileName, Driver_csv_file)
        with open("File_name_file.txt",'w') as f:
            f.write(newFileName)
            f.close()
        colorama.AnsiToWin32.stream = None
        os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"      
        cmd = ["python","manage.py", "runscript",'DriverCsvToModel.py']
        subprocess.Popen(cmd,stdout=subprocess.PIPE)
        messages.success(request, "Please wait 5 minutes. The data conversion process continues")
        return redirect('/')
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")