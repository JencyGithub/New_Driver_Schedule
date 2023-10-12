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
    # params = {
    #         'loads': [i+1 for i in range(int(request.session['data'].get('numberOfLoads')))]
    #     }
    params = {
            'loads': [1,2,3]
        }
    return render(request, 'Trip_details/Form2.html',params)