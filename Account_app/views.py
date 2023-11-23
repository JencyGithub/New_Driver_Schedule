from django.shortcuts import render, redirect, get_object_or_404 ,reverse
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import shutil ,json ,os ,tabula ,requests ,colorama ,subprocess ,io ,csv
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
from .models import RCTI
from django.http import Http404
from django.core.serializers.json import DjangoJSONEncoder
from Account_app.reconciliationUtils import *


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

        load_sheet_new_filename = 'Load_Sheet' + time + \
            '!_@' + fileName.replace(" ", "").replace("\t", "")

        lfs = FileSystemStorage(location=load_sheet_folder_path)
        lfs.save(load_sheet_new_filename, loadSheet)

        data = {
            'driverId': request.POST.get('driverId').split('-')[0],
            'clientName': clientName,
            'truckNum': request.POST.get('truckNum').split('-')[0],
            'startTime': request.POST.get('startTime'),
            'endTime': request.POST.get('endTime'),
            'shiftDate': request.POST.get('shiftDate'),
            'loadSheet': load_sheet_new_filename,
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
                fileName = docketFileSave(
                    docket_files, docket_number, returnVal='file_name')

                Docket_file.append(fileName)

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
        BasePlantVal = BasePlant.objects.get_or_create(basePlant="NOT SELECTED")[0]
        for i in range(len(Docket_no)):
            docket_ = DriverDocket(
                tripId=trip,
                # Use the specific value from the list
                docketNumber=Docket_no[i],
                # Use the specific value from the list
                docketFile='static/img/docketFiles/' + Docket_file[i],
                basePlant=BasePlantVal
            )
            docket_.surcharge_type = Surcharge.objects.get_or_create(surcharge_Name = 'Nosurcharge')[0]
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
    rctiErrors = RctiErrors.objects.filter(status = False).values()
    rctiSolve = RctiErrors.objects.filter(status = True).values()
    # return HttpResponse(rctiErrors)
    params = {
        'rctiErrors' : rctiErrors ,
        'rctiSolve' :rctiSolve
    }
    
    return render(request, 'Account/rctiForm.html',params)

def rctiErrorSolve(request ,id):        
    rctiErrorsObj = RctiErrors.objects.get(id = id)
    rctiErrorsObj.status = True
    rctiErrorsObj.save()
    messages.success(request, "Docket status change ")
    return redirect(request.META.get('HTTP_REFERER'))
    

def rctiForm(request, id= None):
    rcti = None
    if id:
        rcti = RCTI.objects.get(id=id)
    params = {
        'rcti': rcti,
    }
    return render(request, 'Account/Tables/rctiForm.html', params)

def convertIntoFloat(str):
    cleaned_string = str.strip('()')
    return float(cleaned_string)

@csrf_protect
def rctiFormSave(request):
    RCTIobj = RCTI()
    RCTIobj.truckNo = request.POST.get('truckNo')
    RCTIobj.docketNumber = request.POST.get('docketNumber')
    RCTIobj.docketDate = request.POST.get('docketDate')
    RCTIobj.docketYard = request.POST.get('docketYard')
    RCTIobj.noOfKm = request.POST.get('noOfKm')
    RCTIobj.cubicMl = request.POST.get('cubicMl')
    RCTIobj.cubicMiAndKmsCost = request.POST.get('cubicMiAndKmsCost')
    RCTIobj.destination = request.POST.get('destination')
    RCTIobj.cartageGSTPayable = request.POST.get('cartageGSTPayable')
    RCTIobj.cartageTotalExGST = request.POST.get('cartageTotalExGST')
    RCTIobj.cartageTotal = request.POST.get('cartageTotal')
    RCTIobj.transferKM = request.POST.get('transferKM')
    RCTIobj.transferKMCost = request.POST.get('transferKMCost')
    RCTIobj.transferKMGSTPayable = request.POST.get('transferKMGSTPayable')
    RCTIobj.transferKMTotalExGST = request.POST.get('transferKMTotalExGST')
    RCTIobj.transferKMTotal = request.POST.get('transferKMTotal')
    RCTIobj.returnKm = request.POST.get('returnKm')
    RCTIobj.returnPerKmPerCubicMeterCost = request.POST.get('returnPerKmPerCubicMeterCost')
    RCTIobj.returnKmGSTPayable = request.POST.get('returnKmGSTPayable')
    RCTIobj.returnKmTotalExGST = request.POST.get('returnKmTotalExGST')
    RCTIobj.returnKmTotal = request.POST.get('returnKmTotal')
    RCTIobj.waitingTimeSCHED = request.POST.get('waitingTimeSCHED')
    RCTIobj.waitingTimeSCHEDCost = request.POST.get('waitingTimeSCHEDCost')
    RCTIobj.waitingTimeSCHEDGSTPayable = request.POST.get('waitingTimeSCHEDGSTPayable')
    RCTIobj.waitingTimeSCHEDTotalExGST = request.POST.get('waitingTimeSCHEDTotalExGST')
    RCTIobj.waitingTimeSCHEDTotal = request.POST.get('waitingTimeSCHEDTotal')
    RCTIobj.waitingTimeInMinutes = request.POST.get('waitingTimeInMinutes')
    RCTIobj.waitingTimeCost = request.POST.get('waitingTimeCost')
    RCTIobj.waitingTimeGSTPayable = request.POST.get('waitingTimeGSTPayable')
    RCTIobj.waitingTimeTotalExGST = request.POST.get('waitingTimeTotalExGST')
    RCTIobj.waitingTimeTotal = request.POST.get('waitingTimeTotal')
    RCTIobj.standByPerHalfHourCost = request.POST.get('standByPerHalfHourCost')
    RCTIobj.standByPerHalfHourDuration = request.POST.get('standByPerHalfHourDuration')
    RCTIobj.standByUnit = request.POST.get('standByUnit')
    RCTIobj.standByGSTPayable = request.POST.get('standByGSTPayable')
    RCTIobj.standByTotalExGST = request.POST.get('standByTotalExGST')
    RCTIobj.standByTotal = request.POST.get('standByTotal')
    RCTIobj.minimumLoad = request.POST.get('minimumLoad')
    RCTIobj.loadCost = request.POST.get('loadCost')
    RCTIobj.minimumLoadGSTPayable = request.POST.get('minimumLoadGSTPayable')
    RCTIobj.minimumLoadTotalExGST = request.POST.get('minimumLoadTotalExGST')
    RCTIobj.minimumLoadTotal = request.POST.get('minimumLoadTotal')
    RCTIobj.surcharge_fixed_normal = request.POST.get('surcharge_fixed_normal')
    RCTIobj.surcharge_fixed_sunday = request.POST.get('surcharge_fixed_sunday')
    RCTIobj.surcharge_fixed_public_holiday = request.POST.get('surcharge_fixed_public_holiday')
    RCTIobj.surcharge_per_cubic_meters_normal = request.POST.get('surcharge_per_cubic_meters_normal')
    RCTIobj.surcharge_per_cubic_meters_sunday = request.POST.get('surcharge_per_cubic_meters_sunday')
    RCTIobj.surcharge_per_cubic_meters_public_holiday = request.POST.get('surcharge_per_cubic_meters_public_holiday')
    RCTIobj.surcharge_duration = request.POST.get('surcharge_duration')
    RCTIobj.surchargeUnit = request.POST.get('surchargeUnit')
    RCTIobj.surchargeGSTPayable = request.POST.get('surchargeGSTPayable')
    RCTIobj.surchargeTotalExGST = request.POST.get('surchargeTotalExGST')
    RCTIobj.surchargeTotal = request.POST.get('surchargeTotal')
    RCTIobj.others = request.POST.get('others')
    RCTIobj.othersCost = request.POST.get('othersCost')
    RCTIobj.othersGSTPayable = request.POST.get('othersGSTPayable')
    RCTIobj.othersTotalExGST = request.POST.get('othersTotalExGST')
    RCTIobj.othersTotal = request.POST.get('othersTotal')
    
    RCTIobj.save()
    
    reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = RCTIobj.docketNumber , docketDate = RCTIobj.docketDate ).first()

    rctiTotalCost =   convertIntoFloat(RCTIobj.cartageTotal) + convertIntoFloat(RCTIobj.waitingTimeTotal) + convertIntoFloat(RCTIobj.transferKMTotal)  +  convertIntoFloat(RCTIobj.returnKmTotal) + convertIntoFloat(RCTIobj.standByTotal) + convertIntoFloat(RCTIobj.minimumLoadTotal)
    
    if not reconciliationDocketObj :
        reconciliationDocketObj = ReconciliationReport()
    
    reconciliationDocketObj.docketNumber =  RCTIobj.docketNumber
    reconciliationDocketObj.docketDate =  RCTIobj.docketDate
    reconciliationDocketObj.rctiLoadAndKmCost =  RCTIobj.cartageTotalExGST
    # reconciliationDocketObj.rctiSurchargeCost =   RCTIobj.docketDate
    reconciliationDocketObj.rctiWaitingTimeCost = RCTIobj.waitingTimeTotal  
    reconciliationDocketObj.rctiTransferKmCost = RCTIobj.transferKMTotal 
    reconciliationDocketObj.rctiReturnKmCost =  RCTIobj.returnKmTotal
    # reconciliationDocketObj.rctiOtherCost =  RCTIobj.docketDate 
    reconciliationDocketObj.rctiStandByCost =  RCTIobj.standByTotal
    reconciliationDocketObj.rctiLoadDeficit =  RCTIobj.minimumLoadTotal
    reconciliationDocketObj.rctiTotalCost =  round(rctiTotalCost,2)
    reconciliationDocketObj.fromRcti = True 
    
    reconciliationDocketObj.save()
    checkMissingComponents(reconciliationDocketObj)
    
    messages.success( request, "RCTI entry successfully done.")
    return redirect('Account:rcti')

@csrf_protect
def rctiSave(request):
    rctiPdf = request.FILES.get('rctiPdf')
    time = getCurrentTimeInString()
    if rctiPdf:
        rctiPdfName = time + "@_!" + (str(rctiPdf.name)).replace(' ','')
        pdfLocation = 'static/Account/RCTI/uplodedRctiPdf'
        savePdfObj = FileSystemStorage(location=pdfLocation)
        savePdfObj.save(rctiPdfName,rctiPdf)
        
    invoiceFile = request.FILES.get('RctiFile')
    save_data = request.POST.get('save')
    
    if not invoiceFile:
        return HttpResponse("No file uploaded")
    try:
        newFileName = time + "@_!" + (str(invoiceFile.name)).replace(' ','')
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
        messages.success( request, "Please wait 5 minutes. The data conversion process continues")
        
        
        return redirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

def uplodedRCTI(request):
   
    rctiFile = os.listdir('static/Account/RCTI/uplodedRctiPdf')
    rctiFileNameLists = []
    for file in rctiFile:
        rctiFileNameLists.append([file.split('@_!')[0],file.split('@_!')[1]])
        
    return render(request, 'Account/uplodedRCTI.html', {'rctiFileNameLists' : rctiFileNameLists})

@csrf_protect
def getRctiError(request):
    rctiErrorData = RctiErrors.objects.filter(pk=request.POST.get('id')).values().first()
    return JsonResponse({'status': True,'data': rctiErrorData})


def expanseForm(request, id = None):
    rctiExpense = None
    if id:
        rctiExpense = RctiExpense.objects.filter(id = id).first()
        rctiExpense.docketDate = dateConverterFromTableToPageFormate(rctiExpense.docketDate)
    params = {
        'rcti' : rctiExpense
    }
    
    return render(request, 'Account/expanseForm.html',params)

@csrf_protect
def expanseSave(request):
    RctiExpenseObj = RctiExpense()
    RctiExpenseObj.truckNo = request.POST.get('truckNo')
    RctiExpenseObj.docketNumber = request.POST.get('docketNumber')
    RctiExpenseObj.docketDate = request.POST.get('docketDate')
    RctiExpenseObj.docketYard = request.POST.get('docketYard')
    RctiExpenseObj.description = request.POST.get('description')
    RctiExpenseObj.paidKm = request.POST.get('paidKm')
    RctiExpenseObj.invoiceQuantity = request.POST.get('invoiceQuantity')
    RctiExpenseObj.unit = request.POST.get('unit')
    RctiExpenseObj.unitPrice = request.POST.get('unitPrice')
    RctiExpenseObj.gstPayable = request.POST.get('gstPayable')
    RctiExpenseObj.totalExGST = request.POST.get('totalExGST')
    RctiExpenseObj.total = request.POST.get('total')
    RctiExpenseObj.save()
    
    messages.success( request, "RCTI Expense Entry successfully done.")
    return redirect('Account:rcti')

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


def driverDocketEntry(request, ids, driverDocketNumber=None , flag = None):
    
    if flag:
        
        return HttpResponse(flag)
    surcharges = Surcharge.objects.all()

    docketData = None
    if driverDocketNumber:
        docketData = DriverDocket.objects.filter(
            docketNumber=driverDocketNumber).first()
        docketData.shiftDate = dateConverterFromTableToPageFormate(docketData.shiftDate)

    driver_trip_id = DriverTrip.objects.filter(id=ids).first()
    if driver_trip_id:
        base_plant = BasePlant.objects.all()
        params = {
            'basePlants': base_plant,
            'id': ids,
            'docketData': docketData,
            'surcharges': surcharges
        }
        return render(request, 'Account/driverDocketEntry.html', params)
    else:
        messages.warning(request, "Invalid Request ")
        return redirect('Account:driverTripsTable')

@csrf_protect
def getSinglePastTripError(request):
    pastTripErrorData = PastTripError.objects.filter(pk=request.POST.get('id')).values().first()
    return JsonResponse({'status': True,'data':pastTripErrorData})

def driverDocketEntrySave(request, ids):
    driver_trip_id = DriverTrip.objects.filter(id=ids).first()
   

    docketNumber_ = int(float(request.POST.get('docketNumber')))
    shiftDate_ = request.POST.get('shiftDate')
    surchargeObj = Surcharge.objects.get(pk=request.POST.get('surcharge_type'))
    try:
        docketNumber = DriverDocket.objects.get(
            docketNumber=docketNumber_, shiftDate=shiftDate_, tripId=driver_trip_id)
        messages.error(request, "This docket number and date already exists!")
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        docketFile = request.FILES.get('docketFile')
        DriverDocketObj = DriverDocket(
            shiftDate=shiftDate_,
            tripId=driver_trip_id,
            docketNumber=docketNumber_,
            docketFile=docketFileSave(docketFile, docketNumber_),
            basePlant=BasePlant.objects.get(pk=request.POST.get('basePlant')),
            noOfKm=request.POST.get('noOfKm'),
            transferKM=request.POST.get('transferKM'),
            surcharge_type=surchargeObj,
            surcharge_duration=request.POST.get('surcharge_duration'),
            cubicMl=request.POST.get('cubicMl'),
            others=request.POST.get('others')
        )

        if request.POST.get('returnToYard') == 'returnToYard':
            DriverDocketObj.returnQty = request.POST.get('returnQty')
            DriverDocketObj.returnKm = request.POST.get('returnKm')
            DriverDocketObj.returnToYard = True
        elif request.POST.get('returnToYard') == 'tippingToYard':
            DriverDocketObj.returnQty = request.POST.get('returnQty')
            DriverDocketObj.returnKm = request.POST.get('returnKm')
            DriverDocketObj.tippingToYard = True

        DriverDocketObj.waitingTimeStart = request.POST.get('waitingTimeStart')
        DriverDocketObj.waitingTimeEnd = request.POST.get('waitingTimeEnd')
        DriverDocketObj.totalWaitingInMinute = getTimeDifference(DriverDocketObj.waitingTimeStart, DriverDocketObj.waitingTimeEnd)
        DriverDocketObj.standByStartTime = request.POST.get('standByStartTime')
        DriverDocketObj.standByEndTime = request.POST.get('standByEndTime')
        DriverDocketObj.comment = request.POST.get('comment')
        DriverDocketObj.save()
        driver_dockets = DriverDocket.objects.filter(tripId=driver_trip_id)

        # Count the number of objects in the queryset
        no_of_loads = driver_dockets.count()
        driver_trip_id.numberOfLoads = no_of_loads

        driver_trip_id.save()
        try:
            errorObj = PastTripError.objects.filter(tripDate=driver_trip_id.shiftDate,truckNo=driver_trip_id.truckNo).first() 
            errorObj.status =False
            errorObj.save()
            # return HttpResponse(errorObj.status)
        except:
            pass
     
        messages.success(request, "Docket Added successfully")
        return redirect('Account:driverTripsTable')


def rctiCsvForm(request):
    BasePlant_ = BasePlant.objects.all()
    return render(request, 'Account/rctiCsvForm.html', {'basePlants': BasePlant_})


def driverSampleCsv(request):
    return FileResponse(open(f'static/Account/sampleDriverEntry.xlsx', 'rb'), as_attachment=True)


@csrf_protect
# @api_view(['POST'])
def rctiTable(request):
    # return HttpResponse(id)
    
    startDate_ = request.POST.get('startDate')
    endDate_ = request.POST.get('endDate')
    basePlant_ = request.POST.get('basePlant')
    docketYard = BasePlant.objects.filter(id = basePlant_).first()
    dataType = request.POST.get('RCTI')


    try:
        if basePlant_:
            if dataType== 'rctiDocket':
                rctiData = RCTI.objects.filter(docketDate__range=(startDate_, endDate_) , docketYard = docketYard).values()
            elif dataType == 'rctiExpense':
                rctiData = RctiExpense.objects.filter(docketDate__range=(startDate_, endDate_), docketYard = docketYard).values()
        else:
            if dataType== 'rctiDocket':
                rctiData = RCTI.objects.filter(docketDate__range=(startDate_, endDate_)).values()
            elif dataType == 'rctiExpense':
                rctiData = RctiExpense.objects.filter(docketDate__range=(startDate_, endDate_)).values()
        params = {
            'RCTIs': rctiData,
            'dataType':dataType
        }
        return render(request, 'Account/Tables/rctiTable.html', params)
    except:
        messages.warning(request, "Invalid Request ")
        return redirect('Account:rctiCsvForm')


def basePlantTable(request):
    basePlants = BasePlant.objects.all()
    locations = Location.objects.all()
    return render(request, 'Account/Tables/basePlantTable.html', {'basePlants': basePlants, 'locations':locations})

def basePlantForm(request, id=None):
    basePlant = location = None
    if id:
        basePlant = BasePlant.objects.get(pk=id)
    params = {
        'basePlant': basePlant,
        'location': location,
    }
    return render(request, "Account/basePlantForm.html", params)

def locationEditForm(request, id=None):
    basePlant = location = None
    if id:
        location = Location.objects.get(pk=id)
    params = {
        'basePlant': basePlant,
        'location': location,
    }
    return render(request, "Account/basePlantForm.html", params)

def locationTable(request):
    locations = Location.objects.all()
    return render(request, 'GearBox/truckForm.html', {'locations': locations})

@csrf_protect
@api_view(['POST'])
def basePlantSave(request, id=None):
    dataList = {
        'basePlant': request.POST.get('basePlant')
    }
    if id:
        updateIntoTable(record_id=id, tableName='BasePlant', dataSet=dataList)
        messages.success(request, 'BasePlant updated successfully')
    else:
        insertIntoTable(tableName='BasePlant', dataSet=dataList)
        messages.success(request, 'BasePlant added successfully')

    return redirect('Account:basePlantTable')

@csrf_protect
@api_view(['POST'])
def locationSave(request, id=None):
    dataList = {
        'location': request.POST.get('location')
    }
    if id:
        updateIntoTable(record_id=id, tableName='Location', dataSet=dataList)
        messages.success(request, 'Location updated successfully')
    else:
        insertIntoTable(tableName='Location', dataSet=dataList)
        messages.success(request, 'Location added successfully')

    return redirect('Account:basePlantTable')


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
        data['clientName_id'] = Client.objects.filter(
            pk=data['clientName_id']).first().name
        data['driverId_id'] = Driver.objects.filter(
            pk=data['driverId_id']).first().name

    return dataset


@csrf_protect
@api_view(['POST'])
def driverTripCsv(request):
    data_list = []
    temp_trip_data_list = []
    temp_docket_data_list = []
    verified_ = request.POST.get('verifiedInput')
    ClientId = request.POST.get('clientInput')
    startDate_values = request.POST.get('startDate').split(',')
    endDate_values = request.POST.get('endDate').split(',')

    if verified_ == '1':
        driver_trip = DriverTrip.objects.filter(verified=True).values()
    elif verified_ == '0':
        driver_trip = DriverTrip.objects.filter(verified=False).values()
    elif ClientId:
        driver_trip = DriverTrip.objects.filter(clientName=ClientId).values()
        foreignKeySet(driver_trip)
    elif request.POST.get('startDate') and request.POST.get('endDate'):
        startDate = date(int(startDate_values[0]), int(
            startDate_values[1]), int(startDate_values[2]))
        endDate = date(int(endDate_values[0]), int(
            endDate_values[1]), int(endDate_values[2]))
        driver_trip = DriverTrip.objects.filter(
            shiftDate__range=(startDate, endDate)).values()
        foreignKeySet(driver_trip)
    else:
        driver_trip = DriverTrip.objects.all().values()

    try:
        for trip in driver_trip:
            temp_trip_data_list.append([
                trip['verified'],
                trip['driverId_id'],
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
            related_dockets = DriverDocket.objects.filter(
                tripId=trip['id']).values_list()
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
                temp_trip_data_list.clear()
    except Exception as e:
        return HttpResponse(e)

    time = str(timezone.now()).replace(':', '').replace(
        '-', '').replace(' ', '').split('.')
    newFileName = time[0]
    location = 'static/Account/DriverTripCsvDownload/'
    lfs = FileSystemStorage(location=location)
    csv_filename = newFileName + '.csv'

    header = ['verified', 'driverId', 'clientName', 'shiftType', 'numberOfLoads', 'truckNo', 'shiftDate', 'startTime', 'endTime', 'loadSheet', 'comment', 'docketId', 'shiftDatetripId', 'tripId', 'docketNumber',
              'docketFile', 'basePlant', 'noOfKm', 'transferKM', 'returnKm', 'waitingTimeInMinutes', 'minimumLoad', 'surcharge_type', 'surcharge_duration', 'cubicMl', 'minLoad', 'standByPerHalfHourDuration', 'others']

    file_name = location + csv_filename

    # Open the CSV file in append mode ('a')
    myFile = open(file_name, 'a', newline='')
    writer = csv.writer(myFile)
    writer.writerow(header)
    writer.writerows(data_list)
    myFile.close()
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
    dataList = DriverTrip.objects.filter(
        clientName=request.POST.get('id')).values()
    foreignKeySet(dataList)
    return JsonResponse({'status': True, 'data': list(dataList)})


@api_view(['POST'])
def dateRangeFilter(request):
    startDate_values = request.POST.getlist('startDate[]')
    endDate_values = request.POST.getlist('endDate[]')
    startDate = date(int(startDate_values[0]), int(
        startDate_values[1]), int(startDate_values[2]))
    endDate = date(int(endDate_values[0]), int(
        endDate_values[1]), int(endDate_values[2]))
    dataList = DriverTrip.objects.filter(
        shiftDate__range=(startDate, endDate)).values()
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
    surcharges = Surcharge.objects.all()
    count_ = 1
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
        'trucks': AdminTrucks,
        'surcharges' : surcharges
    }
    return render(request, 'Account/Tables/DriverTrip&Docket/tripEditForm.html', params)


@csrf_protect
def driverEntryUpdate(request, ids):
    # Update Trip Save
    driver_trip = DriverTrip.objects.get(id=ids)

    driver_trip.verified = True if request.POST.get('verified') == 'on' else False
    driver_trip.driverId = Driver.objects.get(pk=request.POST.get('driverId'))
    driver_trip.clientName = Client.objects.get(
        pk=request.POST.get('clientName'))
    driver_trip.shiftType = request.POST.get('shiftType')
    driver_trip.numberOfLoads = request.POST.get('numberOfLoads')
    driver_trip.truckNo = request.POST.get('truckNo')
    driver_trip.shiftDate = request.POST.get('shiftDate')
    driver_trip.startTime = request.POST.get('startTime')
    driver_trip.endTime = request.POST.get('endTime')
    if request.FILES.get('loadSheet'):
        loadSheet = request.FILES.get('loadSheet')
        driver_trip.loadSheet = loadFileSave(loadSheet)

    driver_trip.comment = request.POST.get('comment')
    driver_trip.save()

    driver_docket = DriverDocket.objects.filter(tripId=ids).values()
    count_ = 0
    for i in driver_docket:
        try:
            docketNumberVal = DriverDocket.objects.get(docketNumber=int(float(request.POST.get(f'docketNumber{count_}'))), shiftDate=request.POST.get(f'shiftDate{count_}'))
            if docketNumberVal.docketId != i['docketId']:
                messages.error(request, "Docket must be unique.")
                return redirect(request.META.get('HTTP_REFERER'))
        except:
            pass
        docketObj = DriverDocket.objects.get(pk=i['docketId'])
        docketObj.shiftDate = request.POST.get(f'shiftDate{count_}')
        docketObj.docketNumber = int(float(request.POST.get(f'docketNumber{count_}')))
        if request.FILES.get(f'docketFile{count_}'):
            docketFiles = request.FILES.get(f'docketFile{count_}')
            docketObj.docketFile = docketFileSave(
                docketFiles, docketObj.docketNumber)
        docketObj.basePlant = BasePlant.objects.get(
            pk=request.POST.get(f'basePlant{count_}'))
        docketObj.noOfKm = request.POST.get(f'noOfKm{count_}')
        docketObj.transferKM = request.POST.get(f'transferKM{count_}')
        surchargeObj = Surcharge.objects.get(pk = request.POST.get(f'surcharge_type{count_}'))
        docketObj.surcharge_type = surchargeObj
        if request.POST.get(f'returnToYard{count_}') == f'returnToYard{count_}':
            docketObj.returnQty = request.POST.get(f'returnQty{count_}')
            docketObj.returnKm = request.POST.get(f'returnKm{count_}')
            docketObj.returnToYard = True
        elif request.POST.get(f'returnToYard{count_}') == f'tippingToYard{count_}':
            docketObj.returnQty = request.POST.get(f'returnQty{count_}')
            docketObj.returnKm = request.POST.get(f'returnKm{count_}')
            docketObj.tippingToYard = True
        
        docketObj.waitingTimeStart = request.POST.get(
            f'waitingTimeStart{count_}')
        docketObj.waitingTimeEnd = request.POST.get(f'waitingTimeEnd{count_}')
        docketObj.totalWaitingInMinute = getTimeDifference(
            docketObj.waitingTimeStart, docketObj.waitingTimeEnd)
        docketObj.surcharge_duration = request.POST.get(
            f'surcharge_duration{count_}')
        docketObj.cubicMl = request.POST.get(f'cubicMl{count_}')
        docketObj.standByStartTime = request.POST.get(
            f'standByStartTime{count_}')
        docketObj.standByEndTime = request.POST.get(f'standByEndTime{count_}')
        docketObj.others = request.POST.get(f'others{count_}')
        docketObj.comment = request.POST.get(f'comment{count_}')
        count_ += 1
        docketObj.save()
        
        if driver_trip.verified:
            docketObj.shiftDate= datetime.strptime(docketObj.shiftDate, "%Y-%m-%d").date()
            driverDocketNumber = docketObj.docketNumber
            reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = driverDocketNumber , docketDate = docketObj.shiftDate ).first()
                    
            if not  reconciliationDocketObj :
                reconciliationDocketObj = ReconciliationReport()
                
             
            reconciliationDocketObj.driverId = request.POST.get('driverId')  
            reconciliationDocketObj.clientId = request.POST.get('clientName') 
            reconciliationDocketObj.truckId = request.POST.get('truckNo') 
                
            driverLoadAndKmCost = checkLoadAndKmCost(driverDocketNumber,docketObj.shiftDate)
            driverSurchargeCost = checkSurcharge(driverDocketNumber,docketObj.shiftDate)
            # return HttpResponse(driverSurchargeCost)
            driverWaitingTimeCost = checkWaitingTime(driverDocketNumber,docketObj.shiftDate)
            driverStandByCost = checkStandByTotal(driverDocketNumber,docketObj.shiftDate)
            driverTransferKmCost = checkTransferCost(driverDocketNumber,docketObj.shiftDate)
            driverReturnKmCost = checkReturnCost(driverDocketNumber,docketObj.shiftDate)
            # minLoad 
            driverLoadDeficit = checkMinLoadCost(driverDocketNumber,docketObj.shiftDate)
            # TotalCost 
            driverTotalCost = driverLoadAndKmCost +driverSurchargeCost + driverWaitingTimeCost + driverStandByCost + driverTransferKmCost + driverReturnKmCost +driverLoadDeficit
            reconciliationDocketObj.docketNumber = driverDocketNumber  
            reconciliationDocketObj.docketDate = docketObj.shiftDate  
            reconciliationDocketObj.driverLoadAndKmCost = driverLoadAndKmCost 
            reconciliationDocketObj.driverSurchargeCost = driverSurchargeCost 
            reconciliationDocketObj.driverWaitingTimeCost = driverWaitingTimeCost 
            reconciliationDocketObj.driverStandByCost = driverStandByCost 
            reconciliationDocketObj.driverLoadDeficit = driverLoadDeficit 
            reconciliationDocketObj.driverTransferKmCost = driverTransferKmCost 
            reconciliationDocketObj.driverReturnKmCost = driverReturnKmCost  
            reconciliationDocketObj.driverTotalCost = round(driverTotalCost,2)
            reconciliationDocketObj.fromDriver = True 
            reconciliationDocketObj.save()
            # missingComponents 
            checkMissingComponents(reconciliationDocketObj)
    # return HttpResponse('Work')
    messages.success(request, "Data updated successfully")
    return redirect('Account:driverTripsTable')


# ````````````````````````````````````
# Reconciliation

# ```````````````````````````````````

def reconciliationForm(request, dataType):
    
    drivers = Driver.objects.all()
    clients = Client.objects.all()
    trucks = AdminTruck.objects.all()
    
    params = {
        'drivers': drivers,
        'clients': clients,
        'trucks': trucks ,
    }

    if dataType == 0:
        params['dataType'] = 'Reconciliation Report'
        params['dataTypeInt'] = 0
    elif dataType ==  1:
        params['dataType'] = 'Short paid Report'
        params['dataTypeInt'] = 1
        
        
    return render(request, 'Reconciliation/reconciliation.html', params)

@csrf_protect
def reconciliationAnalysis(request,dataType):
    startDate = dateConvert(request.POST.get('startDate'))
    endDate = dateConvert(request.POST.get('endDate'))
    
    params = {}
    if dataType == 0:
        dataList = ReconciliationReport.objects.filter(docketDate__range=(startDate, endDate),reconciliationType = 0).values()
        params['dataType'] = 'Reconciliation'
        params['dataTypeInt'] = 0
    elif dataType == 1:
        dataList = ReconciliationReport.objects.filter(docketDate__range=(startDate, endDate),reconciliationType = 1).values()
        params['dataType'] = 'Short paid'
        params['dataTypeInt'] = 1
        
    params['dataList'] = dataList
    
    return render(request, 'Reconciliation/reconciliation-result.html', params)
     


def reconciliationDocketView(request, docketNumber):
    # try:
    rctiDocket = RCTI.objects.filter(docketNumber=docketNumber).first()
    # for driverDocket view 
    driverDocket = DriverDocket.objects.filter(docketNumber=docketNumber).first()
    surcharges = Surcharge.objects.all()
    base_plant = BasePlant.objects.all()
    # trip_ = DriverTrip.objects.filter(id = driverDocket.tripId).first()
    # return HttpResponse(trip_)
    # AdminTruckNo = AdminTruck.objects.filter(adminTruckNumber = trip_.truckNo).first()
    # clientTruck = ClientTruckConnection.objects.filter(truckNumber = AdminTruckNo.adminTruckNumber).first()
    # return HttpResponse(clientTruck)
    # rateCard = RateCard.objects.filter(rate_card_name = clientTruck.rate_card_name ).first()
    # return HttpResponse(rateCard)
    
    if rctiDocket:
        rctiDocket.docketDate = dateConverterFromTableToPageFormate(rctiDocket.docketDate)
    if driverDocket:
        driverDocket.shiftDate = dateConverterFromTableToPageFormate(driverDocket.shiftDate)
        driverDocket.docketNumber = str(driverDocket.docketNumber)

    params = {
        'rctiDocket': rctiDocket,
        'driverDocket': driverDocket,
        'surcharges': surcharges,
        'basePlants': base_plant,
    }

    return render(request, 'Reconciliation/reconciliation-docket.html', params)

@csrf_protect
@api_view(['POST'])
def reconciliationSetMark(request):
    dockets = request.POST.getlist('dockets[]')
    for docket in dockets:
        getDocket = ReconciliationReport.objects.filter(docketNumber = docket).first()
        getDocket.reconciliationType = 1
        getDocket.save()
    
    return JsonResponse({'status': True})

def reconciliationEscalationForm(request,id):
    data = ReconciliationReport.objects.filter(pk=id).first()
    data.docketDate = dateConverterFromTableToPageFormate(data.docketDate)
    clientName = Client.objects.filter(pk=data.clientId).first()
    driverDocket = DriverDocket.objects.filter(docketNumber = data.docketNumber).first()
    params = {
        'data':data, 
        'client':clientName,
        'driverDocket' : driverDocket
    }
    return render(request, 'Reconciliation/escalation-form.html',params)


# ```````````````````````````````````
# Public holiday
# ```````````````````````````````````

def publicHoliday(request):
    data = PublicHoliday.objects.all()
    params = {
        'data': data
    }
    return render(request, 'Account/Tables/PublicHoliday.html', params)


def publicHolidayForm(request, id=None):
    data = None
    if id:
        data = PublicHoliday.objects.get(pk=id)
        data.date = dateConverterFromTableToPageFormate(data.date)
    params = {
        'data': data
    }
    return render(request, 'Account/PublicHolidayForm.html', params)


@csrf_protect
@api_view(['POST'])
def publicHolidaySave(request, id=None):
    dataList = {
        'date': request.POST.get('date'),
        'stateName': request.POST.get('state'),
        'description': request.POST.get('description')
    }
    if id:
        updateIntoTable(
            record_id=id, tableName='PublicHoliday', dataSet=dataList)
        messages.success(request, 'Holiday updated successfully')
    else:
        insertIntoTable(tableName='PublicHoliday', dataSet=dataList)
        messages.success(request, 'Holiday added successfully')

    return redirect('Account:publicHoliday')


# ````````````````````````````````````
# Rate Card

# ```````````````````````````````````

def rateCardTable(request):
    RateCards = RateCard.objects.all()
    params = {
        'rateCard': RateCards,
    }
    return render(request, 'Account/Tables/rateCardTable.html', params)


def rateCardForm(request, id=None):

    rateCard = costParameters = thresholdDayShift = thresholdNightShift = grace = onLease = None
    surcharges = Surcharge.objects.all()
    tds = None
    if id:
        rateCard = RateCard.objects.get(pk=id)
        tds = rateCard.tds
        print(rateCard.id)
        costParameters = CostParameters.objects.filter(rate_card_name=rateCard.id).values().last()
        thresholdDayShift = ThresholdDayShift.objects.filter(
            rate_card_name=rateCard.id).values().last()
        thresholdNightShift = ThresholdNightShift.objects.filter(
            rate_card_name=rateCard.id).values().last()
        grace = Grace.objects.filter(
            rate_card_name=rateCard.id).values().last()
        # onLease = OnLease.objects.filter(rate_card_name = rateCard.id, end_date = None).values().first()

        costParameters['start_date'] = dateConverterFromTableToPageFormate(
            costParameters['start_date'])
        thresholdDayShift['start_date'] = dateConverterFromTableToPageFormate(
            thresholdDayShift['start_date'])
        thresholdNightShift['start_date'] = dateConverterFromTableToPageFormate(
            thresholdNightShift['start_date'])
        grace['start_date'] = dateConverterFromTableToPageFormate(
            grace['start_date'])
        # onLease['start_date'] = dateConverterFromTableToPageFormate(onLease['start_date'])

    params = {
        'rateCard': rateCard,
        'costParameters': costParameters,
        'thresholdDayShift': thresholdDayShift,
        'thresholdNightShift': thresholdNightShift,
        'grace': grace,
        'tds': tds,
        # 'onLease' : onLease,
        'surcharges': surcharges
    }
    return render(request, 'Account/rateCardForm.html', params)


@csrf_protect
@api_view(['POST'])
def rateCardSave(request, id=None):
    # print(type(request.POST.get('costParameters_start_date')))
    # return HttpResponse('work')
    # Rate Card
    rateCardID = None
    if not id:
        rateCard = RateCard(rate_card_name=request.POST.get('rate_card_name'))
        tds = float(request.POST.get('rate_card_tds'))
        rateCard.tds = tds
        rateCard.save()
        rateCardID = RateCard.objects.get(
            rate_card_name=request.POST.get('rate_card_name'))
    else:
        rateCardID = RateCard.objects.get(pk=id)

        tds = float(request.POST.get('rate_card_tds'))
        rateCardID.tds = tds
        rateCardID.save()

        oldCostParameters = CostParameters.objects.get(
            rate_card_name=rateCardID.id, end_date=None)
        oldCostParameters.end_date = getYesterdayDate(
            request.POST.get('costParameters_start_date'))
        oldCostParameters.save()

        oldThresholdDayShift = ThresholdDayShift.objects.get(
            rate_card_name=rateCardID.id, end_date=None)
        oldThresholdDayShift.end_date = getYesterdayDate(
            request.POST.get('thresholdDayShift_start_date'))
        oldThresholdDayShift.save()

        oldThresholdNightShift = ThresholdNightShift.objects.get(
            rate_card_name=rateCardID.id, end_date=None)
        oldThresholdNightShift.end_date = getYesterdayDate(
            request.POST.get('thresholdNightShift_start_date'))
        oldThresholdNightShift.save()

        oldGrace = Grace.objects.get(
            rate_card_name=rateCardID.id, end_date=None)
        oldGrace.end_date = getYesterdayDate(
            request.POST.get('grace_start_date'))
        oldGrace.save()

        oldOnLease = OnLease.objects.get(
            rate_card_name=rateCardID.id, end_date=None)
        oldOnLease.end_date = getYesterdayDate(
            request.POST.get('onLease_start_date'))
        oldOnLease.save()

    surchargeObj = Surcharge.objects.get(
        pk=request.POST.get('costParameters_surcharge_type'))
    # CostParameters
    costParameters = CostParameters(
        rate_card_name=rateCardID,
        loading_cost_per_cubic_meter=float(request.POST.get(
            'costParameters_loading_cost_per_cubic_meter')),
        km_cost=float(request.POST.get('costParameters_km_cost')),
        surcharge_type=surchargeObj,
        surcharge_cost=float(request.POST.get(
            'costParameters_surcharge_cost')),
        transfer_cost=float(request.POST.get('costParameters_transfer_cost')),
        return_load_cost=float(request.POST.get(
            'costParameters_return_load_cost')),
        return_km_cost=float(request.POST.get(
            'costParameters_return_km_cost')),
        standby_time_slot_size=float(request.POST.get(
            'costParameters_standby_time_slot_size')),
        standby_cost_per_slot=float(request.POST.get(
            'costParameters_standby_cost_per_slot')),
        waiting_cost_per_minute=float(request.POST.get(
            'costParameters_waiting_cost_per_minute')),
        call_out_fees=float(request.POST.get('costParameters_call_out_fees')),
        demurrage_fees=float(request.POST.get(
            'costParameters_demurrage_fees')),
        cancellation_fees=float(request.POST.get(
            'costParameters_cancellation_fees')),
        start_date=request.POST.get('costParameters_start_date')
    )
    costParameters.save()

    # ThresholdDayShift

    thresholdDayShifts = ThresholdDayShift(
        rate_card_name=rateCardID,
        threshold_amount_per_day_shift=float(request.POST.get(
            'thresholdDayShift_threshold_amount_per_day_shift')),
        loading_cost_per_cubic_meter_included=True if request.POST.get(
            'thresholdDayShift_loading_cost_per_cubic_meter_included') == 'on' else False,
        km_cost_included=True if request.POST.get(
            'thresholdDayShift_km_cost_included') == 'on' else False,
        surcharge_included=True if request.POST.get(
            'thresholdDayShift_surcharge_included') == 'on' else False,
        transfer_cost_included=True if request.POST.get(
            'thresholdDayShift_transfer_cost_included') == 'on' else False,
        return_cost_included=True if request.POST.get(
            'thresholdDayShift_return_cost_included') == 'on' else False,
        standby_cost_included=True if request.POST.get(
            'thresholdDayShift_standby_cost_included') == 'on' else False,
        waiting_cost_included=True if request.POST.get(
            'thresholdDayShift_waiting_cost_included') == 'on' else False,
        call_out_fees_included=True if request.POST.get(
            'thresholdDayShift_call_out_fees_included') == 'on' else False,
        min_load_in_cubic_meters=float(request.POST.get(
            'thresholdDayShift_min_load_in_cubic_meters')),
        min_load_in_cubic_meters_return_to_yard=float(request.POST.get(
            'thresholdDayShift_min_load_in_cubic_meters_return_to_yard')),
        return_to_yard_grace=float(request.POST.get(
            'thresholdDayShift_return_to_yard_grace')),
        return_to_tipping_grace=float(request.POST.get(
            'thresholdDayShift_return_to_tipping_grace')),
        start_date=request.POST.get('thresholdDayShift_start_date')
    )
    thresholdDayShifts.save()

    # ThresholdNightShift
    thresholdNightShifts = ThresholdNightShift(
        rate_card_name=rateCardID,
        threshold_amount_per_night_shift=request.POST.get(
            'thresholdNightShift_threshold_amount_per_night_shift'),
        loading_cost_per_cubic_meter_included=True if request.POST.get(
            'thresholdNightShift_loading_cost_per_cubic_meter_included') == 'on' else False,
        km_cost_included=True if request.POST.get(
            'thresholdNightShift_km_cost_included') == 'on' else False,
        surcharge_included=True if request.POST.get(
            'thresholdNightShift_surcharge_included') == 'on' else False,
        transfer_cost_included=True if request.POST.get(
            'thresholdNightShift_transfer_cost_included') == 'on' else False,
        return_cost_included=True if request.POST.get(
            'thresholdNightShift_return_cost_included') == 'on' else False,
        standby_cost_included=True if request.POST.get(
            'thresholdNightShift_standby_cost_included') == 'on' else False,
        waiting_cost_included=True if request.POST.get(
            'thresholdNightShift_waiting_cost_included') == 'on' else False,
        call_out_fees_included=True if request.POST.get(
            'thresholdNightShift_call_out_fees_included') == 'on' else False,
        min_load_in_cubic_meters=float(request.POST.get(
            'thresholdNightShift_min_load_in_cubic_meters')),
        min_load_in_cubic_meters_return_to_yard=float(request.POST.get(
            'thresholdNightShift_min_load_in_cubic_meters_return_to_yard')),
         return_to_yard_grace=float(request.POST.get(
            'thresholdNightShift_return_to_yard_grace')),
        return_to_tipping_grace=float(request.POST.get(
            'thresholdNightShift_return_to_tipping_grace')),
        start_date=request.POST.get('thresholdNightShift_start_date')
    )
    thresholdNightShifts.save()

    # Grace
    grace = Grace(
        rate_card_name=rateCardID,
        load_km_grace=request.POST.get('grace_load_km_grace'),
        transfer_km_grace=float(request.POST.get('grace_transfer_km_grace')),
        return_km_grace=float(request.POST.get('grace_return_km_grace')),
        standby_time_grace_in_minutes=float(
            request.POST.get('grace_standby_time_grace_in_minutes')),
        chargeable_standby_time_starts_after=float(
            request.POST.get('grace_chargeable_standby_time_starts_after')),
        waiting_time_grace_in_minutes=float(
            request.POST.get('grace_waiting_time_grace_in_minutes')),
        chargeable_waiting_time_starts_after=float(
            request.POST.get('grace_chargeable_waiting_time_starts_after')),
        start_date=request.POST.get('grace_start_date')
    )
    grace.save()

    # onLease = OnLease(
    #     rate_card_name=rateCardID,
    #     hourly_subscription_charge = float(request.POST.get('onLease_hourly_subscription_charge')),
    #     daily_subscription_charge = float(request.POST.get('onLease_daily_subscription_charge')),
    #     monthly_subscription_charge = float(request.POST.get('onLease_monthly_subscription_charge')),
    #     quarterly_subscription_charge = float(request.POST.get('onLease_quarterly_subscription_charge')),
    #     surcharge_fixed_normal_cost_included = True if request.POST.get('onLease_surcharge_fixed_normal_cost_included') == 'on' else False,
    #     surcharge_fixed_sunday_cost_included = True if request.POST.get('onLease_surcharge_fixed_sunday_cost_included') == 'on' else False,
    #     surcharge_fixed_public_holiday_cost_included = True if request.POST.get('onLease_surcharge_fixed_public_holiday_cost_included') == 'on' else False,
    #     surcharge_per_cubic_meters_normal_cost_included = True if request.POST.get('onLease_surcharge_per_cubic_meters_normal_cost_included') == 'on' else False,
    #     surcharge_per_cubic_meters_sunday_cost_included = True if request.POST.get('onLease_surcharge_per_cubic_meters_sunday_cost_included') == 'on' else False,
    #     surcharge_per_cubic_meters_public_holiday_cost_included = True if request.POST.get('onLease_surcharge_per_cubic_meters_public_holiday_cost_included') == 'on' else False,
    #     transfer_cost_applicable = True if request.POST.get('onLease_transfer_cost_applicable') == 'on' else False,
    #     return_cost_applicable = True if request.POST.get('onLease_return_cost_applicable') == 'on' else False,
    #     standby_cost_per_slot_applicable = True if request.POST.get('onLease_standby_cost_per_slot_applicable') == 'on' else False,
    #     waiting_cost_per_minute_applicable = True if request.POST.get('onLease_waiting_cost_per_minute_applicable') == 'on' else False,
    #     call_out_fees_applicable = True if request.POST.get('onLease_call_out_fees_applicable') == 'on' else False,
    #     start_date = request.POST.get('onLease_start_date')

    # )
    # onLease.save()

    messages.success(request, 'Data successfully add ')
    return redirect('Account:rateCardTable')

# ```````````````````````````````````
# Past trip
# ```````````````````````````````````


def PastTripForm(request):
    pastTripErrors = PastTripError.objects.filter(status = False).values()
    pastTripSolved = PastTripError.objects.filter(status = True).values()
    params = {
       'pastTripErrors' : pastTripErrors ,
       'pastTripSolved' :pastTripSolved
    }
    return render(request, 'Account/pastTrip.html', params)

def pastTripErrorSolve(request, id):
    errorObj = PastTripError.objects.filter(pk=id).first()

    # Try to get the DriverTrip
    tripObj = DriverTrip.objects.filter(shiftDate=errorObj.tripDate, truckNo=errorObj.truckNo).first()

    if tripObj:
        # Convert docketNumber to an integer (if needed)
        docketNumber = round(float(errorObj.docketNumber), 0)

        # Create the parameters dictionary
        params_dict = {
            'ids': tripObj.id,
            'driverDocketNumber': docketNumber,
            'flag': 'True'  # Convert boolean to string
        }

        # Redirect to 'pastTripErrorDocketView' with parameters
        url_name = 'Account:pastTripErrorDocketView'
        return redirect(url_name, **params_dict)
    else:
        # Handle the case where tripObj is None
        return HttpResponse("Error: Trip not found")

    # return redirect(url_name,ids = tripObj.id , driverDocketNumber = docketNumber , flag = 'error')
        # # account_url = reverse('Account:driverDocketEntry', kwargs={'ids': tripObj.id})
        # docketNumber = round(float(errorObj.docketNumber),2)
        # params = {
        #     'ids': tripObj.id,
        #     'driverDocketNumber': docketNumber
        # }
        # account_url = reverse('Account:driverDocketEntry', kwargs= params)
        # # return HttpResponse(account_url)

        # return redirect(account_url)
    # except Exception as e :
    #     print(f'{e}')
    #     return HttpResponse({e})
        
    # return HttpResponse(tripObj)
    

@csrf_protect
@api_view(['POST'])
def pastTripSave(request):
    pastTrip_csv_file = request.FILES.get('pastTripFile')
    if not pastTrip_csv_file:
        return HttpResponse("No file uploaded")
    try:
        time = (str(timezone.now())).replace(':', '').replace(
            '-', '').replace(' ', '').split('.')
        time = time[0]
        
        newFileName = time + "@_!" + (str(pastTrip_csv_file.name)).replace(' ','')

        location = 'static/Account/PastTripsEntry'
        lfs = FileSystemStorage(location=location)
        lfs.save(newFileName, pastTrip_csv_file)
        with open("pastTrip_entry.txt", 'w') as f:
            f.write(newFileName)
            f.close()

        colorama.AnsiToWin32.stream = None
        os.environ["DJANGO_SETTINGS_MODULE"] = "Driver_Schedule.settings"
        cmd = ["python", "manage.py", "runscript", 'PastDataSave.py']
        subprocess.Popen(cmd, stdout=subprocess.PIPE)
        messages.success(request, "Please wait for some time, it takes some time to update the data.")
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


def uplodedPastTrip(request):
   
    pastTripFile = os.listdir('static/Account/PastTripsEntry')
    pasrTripFileNameList = []
    for file in pastTripFile:
        pasrTripFileNameList.append([file.split('@_!')[0],file.split('@_!')[1]])
        
    return render(request, 'Account/uplodedPastTrip.html', {'pasrTripFileNameLists' : pasrTripFileNameList})
# --------------------------------------------
# Surcharge 
# ---------------------------------------------

def surchargeTable(request):
    surcharges = Surcharge.objects.all()
    # return HttpResponse(surcharge_)
    return render(request, 'Account/Tables/surchargeTable.html', {'surcharges': surcharges})


def surchargeForm(request, id=None):
    surcharge = None
    if id:
        surcharge = Surcharge.objects.get(pk=id)

    params = {
        'data': surcharge
    }
    # return HttpResponse(params['data'])
    return render(request, "Account/surchargeForm.html", params)


@csrf_protect
@api_view(['POST'])
def surchargeSave(request, id=None):
    dataList = {
        'surcharge_Name': request.POST.get('surcharge_Name')
    }
    if id is not None:
        updateIntoTable(record_id=id, tableName='Surcharge', dataSet=dataList)
        messages.success(request, 'Surcharge updated successfully')
    else:
        # return HttpResponse(dataList['surcharge_Name'])
        insertIntoTable(tableName='Surcharge', dataSet=dataList)
        messages.success(request, 'Surcharge added successfully')

    return redirect('Account:surchargeTable')