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
import io
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.contrib import messages
from Account_app.models import *
from GearBox_app.models import *
from django.http import FileResponse
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
    loadSheet = request.FILES.get('loadSheet')
    if loadSheet:

        load_sheet_folder_path = 'Temp_Load_Sheet'
        fileName = loadSheet.name
        time = (str(timezone.now())).replace(':', '').replace(
            '-', '').replace(' ', '').split('.')
        time = time[0]

        log_sheet_new_filename = 'Load_Sheet' + time + \
            '!_@' + fileName.replace(" ", "").replace("\t", "")

        lfs = FileSystemStorage(location=load_sheet_folder_path)
        l_filename = lfs.save(log_sheet_new_filename, loadSheet)

        data = {
            'driverId': request.POST.get('driverId').split('-')[0],
            'clientName': clientName,
            'truckNum': request.POST.get('truckNum').split('-')[0],
            'startTime': request.POST.get('startTime'),
            'endTime': request.POST.get('endTime'),
            'shiftDate': request.POST.get('shiftDate'),
            'loadSheet': log_sheet_new_filename,
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
    loadSheet = request.session['data']['loadSheet']
    comment = request.session['data']['comments']
    temp_loadSheet = ''
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

            temp_loadSheet = temp_loadSheet + '-' + docket_number

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

    if not os.path.exists('static/img/finalloadSheet/' + loadSheet):
        shutil.move('Temp_Load_Sheet/' + loadSheet,
                    'static/img/finalloadSheet/' + loadSheet)

    driver = Driver.objects.get(driverId=driverId)

    trip = DriverTrip(
        driverId=driver,
        clientName=clientName,
        shiftType=shiftType,
        numberOfLoads=numberOfLoads,
        truckNo=truckNo,
        startTime=startTime,
        endTime=endTime,
        loadSheet='static/img/finalloadSheet/' + loadSheet,  # Use the filename or None
        comment=comment,
        shiftDate=shiftDate
    )
    trip.save()

    if not request.session['data']['docketGiven']:
        try:
            BasePlantVal = BasePlant.objects.get(basePlant="Not selected")
        except:
            BasePlantObj = BasePlant(
                basePlant="Not selected"
            )
            BasePlantObj.save()
            BasePlantVal = BasePlant.objects.get(basePlant="Not selected")
        for i in range(len(Docket_no)):
            docket_ = DriverDocket(
                tripId=trip,
                # Use the specific value from the list
                docketNumber=Docket_no[i],
                # Use the specific value from the list
                docketFile='static/img/docketFiles/' + Docket_file[i],
                basePlant=BasePlantVal
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


def driverDocketEntry(request, ids):
    base_plant = BasePlant.objects.all()
    params = {
        'basePlants': base_plant,
        'id': ids
    }
    return render(request, 'Account/driverDocketEntry.html', params)


def driverDocketEntrySave(request, ids):

    driver_trip_id = DriverTrip.objects.filter(id=ids).first()
    
    # return HttpResponse(docketNumber)
    # return redirect(request.META.get('HTTP_REFERER'))

    if driver_trip_id:
            try:
                docketNumber = DriverDocket.objects.get(docketNumber = int(float(request.POST.get('docketNumber'))))
                messages.error(request, "This Docket Number already exists for this Trip!")
                return redirect(request.META.get('HTTP_REFERER'))
            except:
                docketFile = request.FILES.get('docketFile')
                time = (str(timezone.now())).replace(':', '').replace( '-', '').replace(' ', '').split('.')
                time = time[0]
                newFileName = 'Load_Sheet' + time + "@_!" + str(docketFile.name)
                location = 'static/img/docketFiles/'

                lfs = FileSystemStorage(location=location)
                lfs.save(newFileName, docketFile)
                # return HttpResponse(location + newFileName)
            DriverDocketObj = DriverDocket(
                shiftDate=request.POST.get('shiftDate'),
                tripId=driver_trip_id,
                docketNumber=int(float(request.POST.get('docketNumber'))),
                docketFile= 'static/img/docketFiles/' + newFileName,
                basePlant=BasePlant.objects.get(pk=request.POST.get('basePlant')),
                noOfKm=request.POST.get('noOfKm'),
                transferKM=request.POST.get('transferKM'),
                returnKm=request.POST.get('returnKm'),
                waitingTimeInMinutes=request.POST.get('waitingTimeInMinutes'),
                minimumLoad=request.POST.get('minimumLoad'),
                surcharge_type=request.POST.get('surcharge_type'),
                surcharge_duration=request.POST.get('surcharge_duration'),
                cubicMl=request.POST.get('cubicMl'),
                minLoad=request.POST.get('minLoad'),
                standByPerHalfHourDuration=request.POST.get('standByPerHalfHourDuration'),
                others=request.POST.get('others')
            )
            DriverDocketObj.save()
            messages.success(request, "Docket Added successfully")
            return redirect('Account:driverTripsTable')            
    else:
        messages.warning(request, "Invalid Request ")
        return redirect('Account:driverTripsTable')


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
        'clientName': clientName
    }
    return render(request, 'Account/Tables/driverTripsTable.html', params)

def foreignKeySet(dataset):
    for data in dataset:
        data['clientName_id'] = Client.objects.filter(pk=data['clientName_id']).first().name
        data['driverId_id'] = Driver.objects.filter(pk=data['driverId_id']).first().name

    return dataset

@csrf_protect
@api_view(['POST'])
def driverTripCsv(request):
    driver_trip = DriverTrip.objects.all()
    data_list = []
    temp_trip_data_list = []
    temp_docket_data_list = []
    verified_ = request.POST.get('verified')
    ClientId = request.POST.get('id_')
    startDate_values = request.POST.getlist('startDate[]')
    endDate_values = request.POST.getlist('endDate[]')
    # print(verified_,ClientId,startDate_values,endDate_values)
    
    if verified_ == '1':
        driver_trip = DriverTrip.objects.filter(verified=True).values()
    elif verified_ == '0':
        driver_trip = DriverTrip.objects.filter(verified=False).values()
    elif ClientId:
        driver_trip = DriverTrip.objects.filter(clientName=request.POST.get('id_')).values()
        foreignKeySet(driver_trip)
    elif startDate_values[0]  != 'NaN' and  endDate_values[1] != 'NaN':
        startDate = date(int(startDate_values[0]), int(startDate_values[1]), int(startDate_values[2]))
        endDate = date(int(endDate_values[0]), int(endDate_values[1]), int(endDate_values[2]))
        driver_trip = DriverTrip.objects.filter(shiftDate__range=(startDate, endDate)).values()
        foreignKeySet(driver_trip)
    else:
        driver_trip = DriverTrip.objects.all()
        
    # print(verified_,ClientId,startDate_values,endDate_values)   
    if verified_   or ClientId    or startDate_values[0]    or endDate_values  :
        try:
            for trip in driver_trip:
                temp_trip_data_list.append([
                    trip['verified'],
                    trip['driverId_id'],  # Access related field using double underscore
                    trip['clientName_id'],
                    trip['shiftType'],
                    trip['numberOfLoads'],
                    trip['truckNo'],
                    trip['shiftDate'],
                    trip['startTime'],
                    trip['endTime'],
                    trip['loadSheet'],
                    trip['comment'],
                ])

                related_dockets = DriverDocket.objects.filter(tripId=trip['id']).values_list()
                if related_dockets:
                    for docket in related_dockets:
                        temp_docket_data_list.append(list(docket))
                    for i in range(len(temp_docket_data_list)):
                        data_list.append( temp_trip_data_list[0] + temp_docket_data_list[i])
                        
                    temp_trip_data_list.clear()
                    temp_docket_data_list.clear()
                else:
                    data_list.extend(temp_trip_data_list)
                    temp_trip_data_list.clear()
        except:
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
                    trip.loadSheet,
                    trip.comment,
                ])
                related_dockets = DriverDocket.objects.filter(tripId=trip.id).values_list()
                if related_dockets:
                    for docket in related_dockets:
                        temp_docket_data_list.append(list(docket))
                    for i in range(len(temp_docket_data_list)):
                        data_list.append( temp_trip_data_list[0] + temp_docket_data_list[i])
                        
                    temp_trip_data_list.clear()
                    temp_docket_data_list.clear()
                else:
                    data_list.extend(temp_trip_data_list)
                    temp_trip_data_list.clear()

    # return HttpResponse(data_list)
    time = str(timezone.now()).replace(':', '').replace(
        '-', '').replace(' ', '').split('.')
    newFileName = time[0]

    location = 'static/Account/DriverTripCsvDownload/'

    lfs = FileSystemStorage(location=location)

    csv_filename = newFileName + '.csv'

    header = ['verified', 'driverId', 'clientName', 'shiftType', 'numberOfLoads', 'truckNo', 'shiftDate', 'startTime', 'endTime', 'loadSheet', 'comment', 'docketId', 'shiftDatetripId', 'tripId', 'docketNumber',
              'docketFile', 'basePlant', 'noOfKm', 'transferKM', 'returnKm', 'waitingTimeInMinutes', 'minimumLoad', 'surcharge_type', 'surcharge_duration', 'cubicMl', 'minLoad', 'standByPerHalfHourDuration', 'others']

    file_name = location + csv_filename
    # return HttpResponse(file_name)

    # Open the CSV file in append mode ('a')
    myFile = open(file_name, 'a', newline='')

    # Create a CSV writer
    writer = csv.writer(myFile)
    writer.writerow(header)
    writer.writerows(data_list)
    myFile.close()
    
    # response = FileResponse(open(file_name, 'rb'), as_attachment=True)
    # response['Content-Disposition'] = f'attachment; filename="{csv_filename}"'
    # return response
    return FileResponse(open(f'static/Account/DriverTripCsvDownload/{csv_filename}', 'rb'), as_attachment=True)
    return FileResponse(open(f'static/Account/DriverTripCsvDownload/{csv_filename}', 'rb'), as_attachment=True)



@csrf_protect
@api_view(['POST'])
def verifiedFilter(request):
    verified = int(request.POST.get('verified'))
    if verified == 1:
        dataList = DriverTrip.objects.filter(verified=True).values()
    else:
        dataList = DriverTrip.objects.filter(verified=False).values()
    foreignKeySet(dataList)
    return JsonResponse({'status': True, 'data': list(dataList)})


@csrf_protect
@api_view(['POST'])
def clientFilter(request):
    dataList = DriverTrip.objects.filter( clientName=request.POST.get('id')).values()
    foreignKeySet(dataList)
    return JsonResponse({'status': True, 'data': list(dataList)})


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


@csrf_protect
def DriverTripEditForm(request, id):
    driver_trip = DriverTrip.objects.get(id=id)
    driver = Driver.objects.all()
    clientName = Client.objects.all()
    AdminTrucks = AdminTruck.objects.all()
    driver_trip.shiftDate = dateConverterFromTableToPageFormate(
        driver_trip.shiftDate)
    driver_docket = DriverDocket.objects.filter(tripId=id)
    count_ = 0
    for i in driver_docket:
        i.shiftDate = dateConverterFromTableToPageFormate(i.shiftDate)
        i.count_ = count_
        count_ += 1
    base_plant = BasePlant.objects.all()

    params = {
        'driverTrip': driver_trip,
        'driverDocket': driver_docket,
        'basePlants': base_plant,
        'Driver': driver,
        'Client': clientName,
        'trucks': AdminTrucks
    }
    return render(request, 'Account/Tables/DriverTrip&Docket/tripEditForm.html', params)


@csrf_protect
def driverEntryUpdate(request, ids):
    # Update Trip Save
    driver_trip = DriverTrip.objects.get(id=ids)

    driver_trip.verified = True if request.POST.get(
        'verified') == 'on' else False
    driver_trip.driverId = Driver.objects.get(pk=request.POST.get('driverId'))
    driver_trip.clientName = Client.objects.get(pk=request.POST.get('clientName'))
    driver_trip.shiftType = request.POST.get('shiftType')
    driver_trip.numberOfLoads = request.POST.get('numberOfLoads')
    driver_trip.truckNo = request.POST.get('truckNo')
    driver_trip.shiftDate = request.POST.get('shiftDate')
    driver_trip.startTime = request.POST.get('startTime')
    driver_trip.endTime = request.POST.get('endTime')
    if request.FILES.get('loadSheet'):
        loadSheet = request.FILES.get('loadSheet')
        time = (str(timezone.now())).replace(':', '').replace(
            '-', '').replace(' ', '').split('.')
        time = time[0]
        newFileName = 'Load_Sheet' + time + "@_!" + str(loadSheet.name)
        location = 'static/img/finalloadSheet/'

        lfs = FileSystemStorage(location=location)
        lfs.save(newFileName, loadSheet)
        driver_trip.loadSheet = 'static/img/finalloadSheet/' + newFileName

    driver_trip.comment = request.POST.get('comment')
    driver_trip.save()
    
    # update Docket Save 
    
    
    
    driver_docket = DriverDocket.objects.filter(tripId=ids).values()
    count_ = 0
    for i in driver_docket:
        docketObj = DriverDocket.objects.get(pk=i['docketId'])
        docketObj.shiftDate = request.POST.get(f'shiftDate{count_}')
        docketObj.docketNumber = int(float(request.POST.get(f'docketNumber{count_}')))
        if request.FILES.get(f'docketFile{count_}'):
            docketFiles = request.FILES.get(f'docketFile{count_}')
            time = (str(timezone.now())).replace(':', '').replace(
                '-', '').replace(' ', '').split('.')
            newFileName = time[0] + "@_!" + str(docketFiles.name)
            location = 'static/img/docketFiles/'

            lfs = FileSystemStorage(location=location)
            lfs.save(newFileName, docketFiles)
            
            docketObj.docketFile = 'static/img/docketFiles/' + newFileName
        docketObj.basePlant = BasePlant.objects.get(
            pk=request.POST.get(f'basePlant{count_}'))
        docketObj.noOfKm = request.POST.get(f'noOfKm{count_}')
        docketObj.transferKM = request.POST.get(f'transferKM{count_}')
        docketObj.returnKm = request.POST.get(f'returnKm{count_}')
        docketObj.waitingTimeInMinutes = request.POST.get(
            f'waitingTimeInMinutes{count_}')
        docketObj.minimumLoad = request.POST.get(f'minimumLoad{count_}')
        docketObj.surcharge_type = request.POST.get(f'surcharge_type{count_}')
        docketObj.surcharge_duration = request.POST.get(
            f'surcharge_duration{count_}')
        docketObj.cubicMl = request.POST.get(f'cubicMl{count_}')
        docketObj.minLoad = request.POST.get(f'minLoad{count_}')
        docketObj.standByPerHalfHourDuration = request.POST.get(
            f'standByPerHalfHourDuration{count_}')
        docketObj.others = request.POST.get(f'others{count_}')

        count_ += 1
        docketObj.save()
    messages.success(request, "Docket updated successfully")
    return redirect('Account:driverTripsTable')


@csrf_protect
def DriverTripEditForm(request, id):
    driver_trip = DriverTrip.objects.get(id=id)
    driver = Driver.objects.all()
    clientName = Client.objects.all()
    AdminTrucks = AdminTruck.objects.all()
    driver_trip.shiftDate = dateConverterFromTableToPageFormate(
        driver_trip.shiftDate)
    driver_docket = DriverDocket.objects.filter(tripId=id)
    count_ = 0
    for i in driver_docket:
        i.shiftDate = dateConverterFromTableToPageFormate(i.shiftDate)
        i.count_ = count_
        count_ += 1
    base_plant = BasePlant.objects.all()

    params = {
        'driverTrip': driver_trip,
        'driverDocket': driver_docket,
        'basePlants': base_plant,
        'Driver': driver,
        'Client': clientName,
        'trucks': AdminTrucks
    }
    return render(request, 'Account/Tables/DriverTrip&Docket/tripEditForm.html', params)


@csrf_protect
def driverEntryUpdate(request, ids):
    # Update Trip Save
    driver_trip = DriverTrip.objects.get(id=ids)

    driver_trip.verified = True if request.POST.get(
        'verified') == 'on' else False
    driver_trip.driverId = Driver.objects.get(pk=request.POST.get('driverId'))
    driver_trip.clientName = Client.objects.get(pk=request.POST.get('clientName'))
    driver_trip.shiftType = request.POST.get('shiftType')
    driver_trip.numberOfLoads = request.POST.get('numberOfLoads')
    driver_trip.truckNo = request.POST.get('truckNo')
    driver_trip.shiftDate = request.POST.get('shiftDate')
    driver_trip.startTime = request.POST.get('startTime')
    driver_trip.endTime = request.POST.get('endTime')
    if request.FILES.get('loadSheet'):
        loadSheet = request.FILES.get('loadSheet')
        time = (str(timezone.now())).replace(':', '').replace(
            '-', '').replace(' ', '').split('.')
        time = time[0]
        newFileName = 'Load_Sheet' + time + "@_!" + str(loadSheet.name)
        location = 'static/img/finalloadSheet/'

        lfs = FileSystemStorage(location=location)
        lfs.save(newFileName, loadSheet)
        driver_trip.loadSheet = 'static/img/finalloadSheet/' + newFileName

    driver_trip.comment = request.POST.get('comment')
    driver_trip.save()
    
    # update Docket Save 
    
    
    
    driver_docket = DriverDocket.objects.filter(tripId=ids).values()
    count_ = 0
    for i in driver_docket:
        docketObj = DriverDocket.objects.get(pk=i['docketId'])
        docketObj.shiftDate = request.POST.get(f'shiftDate{count_}')
        docketObj.docketNumber = int(float(request.POST.get(f'docketNumber{count_}')))
        if request.FILES.get(f'docketFile{count_}'):
            docketFiles = request.FILES.get(f'docketFile{count_}')
            time = (str(timezone.now())).replace(':', '').replace(
                '-', '').replace(' ', '').split('.')
            newFileName = time[0] + "@_!" + str(docketFiles.name)
            location = 'static/img/docketFiles/'

            lfs = FileSystemStorage(location=location)
            lfs.save(newFileName, docketFiles)
            
            docketObj.docketFile = 'static/img/docketFiles/' + newFileName
        docketObj.basePlant = BasePlant.objects.get(
            pk=request.POST.get(f'basePlant{count_}'))
        docketObj.noOfKm = request.POST.get(f'noOfKm{count_}')
        docketObj.transferKM = request.POST.get(f'transferKM{count_}')
        docketObj.returnKm = request.POST.get(f'returnKm{count_}')
        docketObj.waitingTimeInMinutes = request.POST.get(
            f'waitingTimeInMinutes{count_}')
        docketObj.minimumLoad = request.POST.get(f'minimumLoad{count_}')
        docketObj.surcharge_type = request.POST.get(f'surcharge_type{count_}')
        docketObj.surcharge_duration = request.POST.get(
            f'surcharge_duration{count_}')
        docketObj.cubicMl = request.POST.get(f'cubicMl{count_}')
        docketObj.minLoad = request.POST.get(f'minLoad{count_}')
        docketObj.standByPerHalfHourDuration = request.POST.get(
            f'standByPerHalfHourDuration{count_}')
        docketObj.others = request.POST.get(f'others{count_}')

        count_ += 1
        docketObj.save()
    messages.success(request, "Docket updated successfully")
    return redirect('Account:driverTripsTable')


# Reconciliation

def reconciliationForm(request):
    drivers = Driver.objects.all() 
    clients = Client.objects.all() 
    trucks = AdminTruck.objects.all()
    return render(request, 'Reconciliation/reconciliation.html', {'drivers': drivers, 'clients': clients, 'trucks': trucks})


def reconciliationResult(request):
    dataList = request.session['reconciliationResultData']
    params = {
        'dataList' : dataList
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
                'class' : 'bg-danger' if int(i['docketNumber']) not in common_docket else 'bg-success'
           }
       )
    for j in driverDocketList:
        dataList.append(
            {
                'docketNumber' : i['docketNumber'],
                'class' : 'bg-danger' if i['docketNumber'] not in common_docket else 'bg-success'
            }
        )
    request.session['reconciliationResultData'] = dataList

    return redirect('Account:reconciliationResult')

def reconciliationDocketView(request):
    return render(request,'Reconciliation/reconciliation-docket.html')