from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import shutil
import os
import tabula
import requests
import colorama
import subprocess
import csv
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib import messages
from Account_app.models import *
from GearBox_app.models import *
from CRUD import *


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

        params = {
            'client_ids': client_names,
            'admin_truck_no': admin_truck_no,
            'client_truck_no': client_truck_no,
        }
        try:
            Driver_ = Driver.objects.get(email=user_email)
            driver_id = str(Driver_.driverId) + '-' + str(Driver_.name)
            params['driver_ids'] = driver_id
            params['drivers'] = None
            # DriverTruckNum = ClientTruckConnection.objects.get(driverId = Driver_.driverId)
            # params['DriverTruckNum'] = str(DriverTruckNum.clientTruckId) + '-' + str(DriverTruckNum.truckNumber)
            # params['client_names'] = str(DriverTruckNum.clientId.name)

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
    params = {
        'loads': [i+1 for i in range(int(request.session['data'].get('numberOfLoads')))]
    }
    # params = {
    #         'loads': [1,2,3]
    #     }
    return render(request, 'Trip_details/Form2.html', params)

# @csrf_protect
# @api_view(['POST'])


def createFormSession(request):
    clientName = request.POST.get('clientName')
    logSheet = request.FILES.get('logSheet')
    if logSheet:

        load_sheet_folder_path = 'Temp_Load_Sheet'
        fileName = logSheet.name
        time = (str(timezone.now())).replace(':', '').replace(
            '-', '').replace(' ', '').split('.')
        time = time[0]

        log_sheet_new_filename = 'Load_Sheet' + time + \
            '!_@' + fileName.replace(" ", "").replace("\t", "")

        lfs = FileSystemStorage(location=load_sheet_folder_path)
        l_filename = lfs.save(log_sheet_new_filename, logSheet)

        data = {
            'driverId': request.POST.get('driverId').split('-')[0],
            'clientName': clientName,
            'truckNum': request.POST.get('truckNum').split('-')[0],
            'startTime': request.POST.get('startTime'),
            'endTime': request.POST.get('endTime'),
            'shiftDate': request.POST.get('shiftDate'),
            'logSheet': log_sheet_new_filename,
            'shiftType': request.POST.get('shiftType'),
            'numberOfLoads': request.POST.get('numberOfLoads'),
            'comments': request.POST.get('comments')
        }

    data['docketGiven'] = True if Client.objects.get(
        name=clientName).docketGiven else False

    request.session['data'] = data
    # request.session.set_expiry(5)

    return formsSave(request) if Client.objects.get(name=clientName).docketGiven else redirect('Account:getForm2')


# @csrf_protect
# @api_view(['POST'])
def formsSave(request):

    driverId = request.session['data']['driverId']
    clientName = Client.objects.get(name=request.session['data']['clientName'])
    shiftType = request.session['data']['shiftType']
    numberOfLoads = request.session['data']['numberOfLoads']
    truckNo = request.session['data']['truckNum']
    startTime = request.session['data']['startTime']
    endTime = request.session['data']['endTime']
    shiftDate = request.session['data']['shiftDate']
    logSheet = request.session['data']['logSheet']
    comment = request.session['data']['comments']
    temp_logSheet = ''
    Docket_no = []
    Docket_file = []
    time = (str(timezone.now())).replace(':', '').replace(
        '-', '').replace(' ', '').split('.')
    time = time[0]

    if not request.session['data']['docketGiven']:
        for i in range(1, int(numberOfLoads)+1):

            key = f"docketNumber[{i}]"
            docket_number = request.POST.get(key)
            Docket_no.append(docket_number)
            key_files = f"docketFile[{i}]"

            docket_files = request.FILES.get(key_files)

            temp_logSheet = temp_logSheet + '-' + docket_number

            if docket_files:
                # PDF ---------------
                pdf_folder_path = 'static/img/docketFiles'
                fileName = docket_files.name
                # return HttpResponse(fileName.split('.')[-1])
                docket_new_filename = time + '!_@' + \
                    docket_number + '.' + fileName.split('.')[-1]
                # return HttpResponse(docket_new_filename)
                pfs = FileSystemStorage(location=pdf_folder_path)
                pfs.save(docket_new_filename, docket_files)
                Docket_file.append(docket_new_filename)

    if not os.path.exists('static/img/finalLogSheet/' + logSheet):
        shutil.move('Temp_Load_Sheet/' + logSheet,
                    'static/img/finalLogSheet/' + logSheet)

    driver = Driver.objects.get(driverId=driverId)

    trip = DriverTrip(
        driverId=driver,
        clientName=clientName,
        shiftType=shiftType,
        numberOfLoads=numberOfLoads,
        truckNo=truckNo,
        startTime=startTime,
        endTime=endTime,
        logSheet='static/img/finalLogSheet/' + logSheet,  # Use the filename or None
        comment=comment,
        shiftDate=shiftDate
    )
    trip.save()

    if not request.session['data']['docketGiven']:
        for i in range(len(Docket_no)):
            docket_ = DriverDocket(
                tripId=trip,
                # Use the specific value from the list
                docketNumber=Docket_no[i],
                # Use the specific value from the list
                docketFile='static/img/docketFiles/' + Docket_file[i],
                basePlant=BasePlant.objects.get(basePlant="Not selected")
            )
            docket_.save()

    del request.session['data']

    messages.success(request, " Form Successfully Filled Up")
    return redirect('index')


@csrf_protect
@api_view(['POST'])
def getTrucks(request):
    clientName = request.POST.get('clientName')
    # clientName = request.GET.get('clientName')
    client = Client.objects.get(name=clientName)
    truckList = []
    truck_connections = ClientTruckConnection.objects.filter(
        clientId=client.clientId)
    docket = client.docketGiven

    for truck_connection in truck_connections:
        truckList.append(str(truck_connection.truckNumber) +
                         '-' + str(truck_connection.clientTruckId))
    return JsonResponse({'status': True, 'trucks': truckList, 'docket': docket})


def rcti(request):
    return render(request, 'Account/rctiForm.html')


@csrf_protect
def rctiSave(request):
    invoiceFile = request.FILES.get('RctiFile')
    save_data = request.POST.get('save')
    if not invoiceFile:
        return HttpResponse("No file uploaded")
    try:
        time = (str(timezone.now())).replace(':', '').replace(
            '-', '').replace(' ', '').split('.')
        time = time[0]
        newFileName = time + "@_!" + str(invoiceFile.name)
        location = 'static/Account/RCTI/tempRCTIInvoice'

        lfs = FileSystemStorage(location=location)
        lfs.save(newFileName, invoiceFile)

        cmd = ["python", "Account_app/utils.py", newFileName]
        subprocess.Popen(cmd, stdout=subprocess.PIPE)
        # return HttpResponse('work')
        if save_data == '1':
            colorama.AnsiToWin32.stream = None
            os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
            cmd = ["python", "manage.py", "runscript", 'csvToModel.py']
            subprocess.Popen(cmd, stdout=subprocess.PIPE)
        messages.success(
            request, "Please wait 5 minutes. The data conversion process continues")
        return redirect('Account:index')
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


def driverEntry(request):
    return render(request, 'Account/driverEntryForm.html')


@csrf_protect
def driverEntrySave(request):
    Driver_csv_file = request.FILES.get('driverEntryFile')
    if not Driver_csv_file:
        return HttpResponse("No file uploaded")
    try:
        time = (str(timezone.now())).replace(':', '').replace(
            '-', '').replace(' ', '').split('.')
        time = time[0]
        newFileName = time + "@_!" + str(Driver_csv_file.name)
        location = 'static/Account/DriverEntry'

        lfs = FileSystemStorage(location=location)
        lfs.save(newFileName, Driver_csv_file)
        with open("Driver_reg_file.txt", 'w') as f:
            f.write(newFileName)
            f.close()
        colorama.AnsiToWin32.stream = None
        os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
        cmd = ["python", "manage.py", "runscript", 'DriverCsvToModel.py']
        subprocess.Popen(cmd, stdout=subprocess.PIPE)
        messages.success(
            request, "Please wait 5 minutes. The data conversion process continues")
        return redirect('Account:index')
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


def rctiTable(request):
    RCTI_ = RCTI.objects.all()
    return render(request, 'Account/Tables/rctiTable.html', {'RCTI': RCTI_})


def basePlantTable(request):
    basePlant_ = BasePlant.objects.all()
    return render(request, 'Account/Tables/basePlantTable.html', {'BP_': basePlant_})


def driverTripsTable(request):
    driver_trip = DriverTrip.objects.all()
    clientName = Client.objects.all()
    params = {
        'driverTrip': driver_trip,
        'clientName' : clientName
    }
    return render(request, 'Account/Tables/driverTripsTable.html', params)


def driverTripCsv(request):
    driver_trip = DriverTrip.objects.all()
    data_list = []
    temp_trip_data_list = []
    temp_docket_data_list = []

    for trip in driver_trip:
        temp_trip_data_list.append([
            trip.verified,
            trip.driverId.name,
            trip.clientName,
            trip.shiftType,
            trip.numberOfLoads,
            trip.truckNo,
            trip.shiftDate,
            trip.startTime,
            trip.endTime,
            trip.logSheet,
            trip.comment,
        ])
        related_dockets = DriverDocket.objects.filter(
            tripId=trip.id).values_list()
        if related_dockets:
            for docket in related_dockets:
                temp_docket_data_list.append(list(docket))

            for i in range(len(temp_docket_data_list)):
                data_list.append(
                    temp_trip_data_list[0] + temp_docket_data_list[i])
            temp_trip_data_list.clear()
            temp_docket_data_list.clear()
        else:
            data_list.extend(temp_trip_data_list)

    time = str(timezone.now()).replace(':', '').replace(
        '-', '').replace(' ', '').split('.')
    newFileName = time[0]

    location = 'static/Account/DriverTripCsvDownload/'

    lfs = FileSystemStorage(location=location)

    csv_filename = newFileName + '.csv'

    header = ['verified','driverId', 'clientName', 'shiftType', 'numberOfLoads', 'truckNo', 'shiftDate', 'startTime', 'endTime', 'logSheet', 'comment', 'docketId', 'tripId', 'shiftDate', 'docketNumber', 'docketFile', 'basePlant', 'noOfKm', 'transferKM', 'returnKm', 'waitingTimeInMinutes', 'minimumLoad','surcharge_type', 'surcharge_duration', 'cubicMl', 'minLoad', 'standByPerHalfHourDuration', 'others']

    file_name = location + csv_filename

    # Open the CSV file in append mode ('a')
    myFile = open(file_name, 'a', newline='')

    # Create a CSV writer
    writer = csv.writer(myFile)
    writer.writerow(header)
    writer.writerows(data_list)
    myFile.close()
    messages.success(
            request, "Csv Complete")
    return redirect('Account:index')


def foreignKeySet(dataset):
    for data in dataset:
        data['clientName_id'] = Client.objects.filter(pk = data['clientName_id']).first().name
        data['driverId_id'] = Driver.objects.filter(pk = data['driverId_id']).first().name
        
    return dataset

@csrf_protect
@api_view(['POST'])
def verifiedFilter(request):
    verified = int(request.POST.get('verified'))
    if verified == 1 :
        dataList = DriverTrip.objects.filter(verified=True).values()
    else:
        dataList = DriverTrip.objects.filter(verified=False).values()
    foreignKeySet(dataList)          
    return JsonResponse({'status' : True,'data' : list(dataList)})

@csrf_protect
@api_view(['POST'])
def clientFilter(request):
    dataList = DriverTrip.objects.filter(clientName = request.POST.get('id')).values()
    foreignKeySet(dataList)
    return JsonResponse({'status' : True,'data' : list(dataList)})

# @csrf_protect
# @api_view(['POST'])
# def dateRangeFilter(request):
#     print(request.POST)
#     startDate = request.POST.getlist('startDate[]')
#     endDate = request.POST.getlist('endDate[]')
#     startDate = date(int(startDate[0]),int(startDate[1]),int(startDate[2]))
#     endDate =  date(int(endDate[0]),int(endDate[1]),int(endDate[2]))
#     print(startDate,endDate)
#     dataList = DriverTrip.objects.filter(shiftDate__range=[startDate,endDate])
#     foreignKeySet(dataList)
#     return JsonResponse({'status' : True,'data' : list(dataList)})
    
    
@api_view(['POST'])
def dateRangeFilter(request):
    print(request.POST)
    startDate_values = request.POST.getlist('startDate[]')
    endDate_values = request.POST.getlist('endDate[]')
    startDate = date(int(startDate_values[0]), int(startDate_values[1]), int(startDate_values[2]))
    endDate = date(int(endDate_values[0]), int(endDate_values[1]), int(endDate_values[2]))
    dataList = DriverTrip.objects.filter(shiftDate__range=(startDate, endDate)).values()
    foreignKeySet(dataList)
    return JsonResponse({'status': True, 'data': list(dataList)})


# Reconciliation

def reconciliationForm(request):
    drivers = Driver.objects.all() 
    clients = Client.objects.all() 
    trucks = AdminTruck.objects.all()
    return render(request, 'Reconciliation/reconciliation.html', {'drivers': drivers, 'clients': clients, 'trucks': trucks})


def reconciliationResult(request):
    dataList = request.session['reconciliationResultData']
    basePlants = BasePlant.objects.all() 
    params = {
        'dataList' : dataList,
        'basePlants' : basePlants
    }
    return render(request, 'Reconciliation/reconciliation-result.html',params)

@csrf_protect
@api_view(['POST'])
def reconciliationAnalysis(request):
    startDate = dateConvert(request.POST.get('startDate'))
    endDate =dateConvert(request.POST.get('endDate')) 
    driverDocketList = DriverDocket.objects.filter(shiftDate__range=(startDate, endDate)).values()
    RCTIList = RCTI.objects.filter(docketDate__range=(startDate, endDate)).values()
    unique_RCTI = {int(item['docketNumber']) for item in RCTIList}
    unique_driverDocket = {item['docketNumber'] for item in driverDocketList}
    common_docket = unique_RCTI.intersection(unique_driverDocket)

    dataList = []


    for i in RCTIList:
       dataList.append(
           {
               'docketNumber' : int(i['docketNumber']),
                'class' : 'text-danger' if int(i['docketNumber']) not in common_docket else 'text-success'
           }
       )
    for j in driverDocketList:
        dataList.append(
            {
                'docketNumber' : i['docketNumber'],
                'class' : 'text-danger' if i['docketNumber'] not in common_docket else 'text-success'
            }
        )
    request.session['reconciliationResultData'] = dataList

    return redirect('Account:reconciliationResult')

def reconciliationDocketView(request):
    return render(request,'Reconciliation/reconciliation-docket.html')