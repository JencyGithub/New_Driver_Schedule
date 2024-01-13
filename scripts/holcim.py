from Account_app.models import *
import pandas as pd
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
from Account_app.reconciliationUtils import  *
from datetime import time

def dateConvert(dataList,type_):
    try:
        if dataList.lower() != 'nan':
            timestamp_obj = datetime.strptime(dataList, '%d/%m/%Y %I:%M:%S %p')
            if type_ =='date':
                date_only_str = timestamp_obj.strftime('%Y-%m-%d')
                return date_only_str
            elif type_ == 'time':
                time_only_str = timestamp_obj.strftime('%H:%M:%S')
                return time_only_str
        else:
            date_only_str = None  
        return date_only_str
    except Exception as e:
        return None
    

def dateTimeConvert(dataList):
    try:
        if pd.isna(dataList) or str(dataList).lower() == 'nan':
            return None
        else:
            try:
                timestamp_obj = datetime.strptime(str(dataList),  '%Y-%m-%d %H:%M:%S')
            except: 
                timestamp_obj = datetime.strptime(str(dataList), '%d/%m/%Y %I:%M:%S %p')
            formatted_timestamp = timestamp_obj.strftime('%Y-%m-%d %H:%M:%S')
            return formatted_timestamp
    except ValueError as e:
        return None
    
    
    

with open("File_name_file.txt", 'r') as f:
    file_names = f.read().split('<>') 

monthFileName = open(r"pastTrip_entry_month.txt",'r')
monthAndYear = monthFileName.read()
primaryFile = f'static/Account/RCTI/Report/{file_names[0].strip()}'
secondaryFile = f'static/Account/RCTI/Report/{file_names[1].strip()}'
# print(primaryFile)

count_ = 0
data = pd.read_excel(primaryFile)
for index, row in data.iterrows():
    driverId = None
    try:
        count_ +=1
        tripDate = row[1]
        if row[3] == 'nan':
            pastTripErrorObj = PastTripError(
                clientName = 'holcim',
                tripDate = tripDate,
                docketNumber = None,
                truckNo = int(row[2]),
                lineNumber = count_,
                errorFromPastTrip = 'Job No. Missing.',
                fileName = primaryFile.split('@_!')[-1],
                data = str(row) ,
                errorType = 1
            )
            pastTripErrorObj.save()
            continue
        if str(row[10]) != 'nan':
            driverId = Driver.objects.filter(name = row[10].strip().replace(' ','').lower()).first()
        if driverId is None:
            pastTripErrorObj = PastTripError(
                clientName = 'holcim',
                tripDate = tripDate,
                docketNumber = str(row[3]),
                truckNo = int(row[2]),
                lineNumber = count_,
                errorFromPastTrip = 'Driver matching query does not exist.',
                fileName = primaryFile.split('@_!')[-1],
                data = str(row) ,
                errorType = 1
            )
            pastTripErrorObj.save()
            continue
        
        existingTrip = HolcimTrip.objects.filter(truckNo = int(row[2]) , shiftDate = tripDate).values().first()
        if existingTrip:
            holcimTripObj = HolcimTrip.objects.get(pk=existingTrip['id'])
        else:
            holcimTripObj = HolcimTrip(
                truckNo = int(row[2]),
                shiftDate = tripDate
            )
            holcimTripObj.save()
        existingDockets = HolcimDocket.objects.filter(tripId = holcimTripObj.id).count()
        currentMatchingDocket = HolcimDocket.objects.filter(tripId =  holcimTripObj.id,jobNo = row[3] ,docketDate = tripDate).first()
        if currentMatchingDocket:
            pastTripErrorObj = PastTripError(
            clientName = 'holcim',
            tripDate = tripDate,
            docketNumber = str(row[3]),
            truckNo = int(row[2]),
            lineNumber = count_,
            errorFromPastTrip = 'Docket already exist.',
            fileName = primaryFile.split('@_!')[-1],
            data = str(row) ,
            errorType = 1
            )
            pastTripErrorObj.save()
            continue
        client = Client.objects.filter(name = 'holcim').first()
        adminTruckObj = AdminTruck.objects.filter(adminTruckNumber = holcimTripObj.truckNo).first()
        clientTruckConnectionObj = ClientTruckConnection.objects.filter(truckNumber = adminTruckObj,startDate__lte = holcimTripObj.shiftDate,endDate__gte = holcimTripObj.shiftDate, clientId = client).first()       
        if clientTruckConnectionObj is None:
            pastTripErrorObj = PastTripError(
                clientName = 'holcim',
                tripDate = tripDate,
                docketNumber = str(row[3]),
                truckNo = int(row[2]),
                lineNumber = count_,
                errorFromPastTrip = 'Client truck connection object does not exist.',
                fileName = primaryFile.split('@_!')[-1],
                data = str(row) ,
                errorType = 1
            )
            pastTripErrorObj.save()
            continue
        basePlantObj = BasePlant.objects.filter(basePlant = row[5].strip().upper()).first()
        if basePlantObj is None:
            pastTripErrorObj = PastTripError(
                clientName = 'holcim',
                tripDate = tripDate,
                docketNumber = str(row[3]),
                truckNo = int(row[2]),
                lineNumber = count_,
                errorFromPastTrip = 'BasePlant does not exist.',
                fileName = primaryFile.split('@_!')[-1],
                data = str(row) ,
                errorType = 1
            )
            pastTripErrorObj.save()
            continue
        holcimDocketObj = HolcimDocket()
        holcimDocketObj.truckNo  = int(row[2])
        holcimDocketObj.tripId  = holcimTripObj
        holcimDocketObj.docketDate  = tripDate
        holcimDocketObj.jobNo  =  row[3]
        holcimDocketObj.orderNo = row[4]
        holcimDocketObj.basePlant = basePlantObj
        holcimDocketObj.materialCode = 0 if str(row[9]) == 'nan' else row[9] 
        holcimDocketObj.customerName =  0 if str(row[6] ) == 'nan' else row[6] 
        holcimDocketObj.address =  0 if str(row[7]) == 'nan' else row[7]
        holcimDocketObj.loadSize =  0 if str(row[8]) == 'nan' else row[8]
        holcimDocketObj.timeOnSite =  0 if str(row[11]) == 'nan' else row[11]
        holcimDocketObj.distanceInKm =  0 if str(row[12]) == 'nan' else row[12]
        holcimDocketObj.requestedKm =  0 if str(row[13]) == 'nan' else row[13]
        holcimDocketObj.reasonRequested =  0 if str(row[14]) == 'nan' else row[14]
        holcimDocketObj.returnedQty =  0 if str(row[15]) == 'nan' else row[15]
        holcimDocketObj.dischargeLocation =  0 if str(row[16]) == 'nan' else row[16]
        holcimDocketObj.additionalKm =  0 if str(row[17]) == 'nan' else row[17]
        holcimDocketObj.driverName = driverId
        holcimDocketObj.status =  0 if str(row[18]) == 'nan' else row[18]
        holcimDocketObj.save()
        holcimTripObj.numberOfLoads = existingDockets + 1
        holcimTripObj.save()
        
    except Exception as e:
        pastTripErrorObj = PastTripError(
            clientName = 'holcim',
                tripDate = tripDate,
                docketNumber = str(row[3]),
                truckNo = int(row[2]),
                lineNumber = count_,
                errorFromPastTrip = e,
                fileName = primaryFile.split('@_!')[-1],
                data = str(row) ,
                errorType = 1
        )
        pastTripErrorObj.save()
        
count = 0
secondaryData = pd.read_excel(secondaryFile)
for index , row in secondaryData.iterrows():
    flag = False
    holcimDocketObj = None
    count += 1
    try:
        int(row[0])
        int(row[2])
        flag = True
    except:
        flag = False
        
    if flag:
        try:
            tripDate = dateConvert(str(row[8]),'date')
            tripDate = datetime.strptime(tripDate, '%Y-%m-%d').date()
            try:
                existingTrip = HolcimTrip.objects.filter(truckNo = float(row[0]) ,shiftDate = tripDate).first()
                holcimDocketObj = HolcimDocket.objects.filter(tripId = existingTrip.id, jobNo = float(row[4])).first()
            except Exception as e:
                pastTripErrorObj = PastTripError(
                    clientName = 'holcim',
                    tripDate = tripDate,
                    docketNumber = str(row[4]),
                    truckNo = int(row[0]),
                    lineNumber = count_,
                    errorFromPastTrip = 'Docket number not exist in primary files.',
                    fileName = secondaryFile.split('@_!')[-1],
                    data = str(row) ,
                    errorType = 1
                )
                pastTripErrorObj.save()
                continue
            
            
            if holcimDocketObj is None:
                pastTripErrorObj = PastTripError(
                    clientName = 'holcim',
                    tripDate = tripDate,
                    docketNumber = str(row[4]),
                    truckNo = int(row[0]),
                    lineNumber = count_,
                    errorFromPastTrip = 'Docket number not exist in primary files.',
                    fileName = secondaryFile.split('@_!')[-1],
                    data = str(row) ,
                    errorType = 1
                )
                pastTripErrorObj.save()
                continue
            
            holcimDocketObj.orderNo  = 0 if str(row[2]) == 'nan' else row[2]
            holcimDocketObj.status  = 0 if str(row[6]) == 'nan' else row[6]
            holcimDocketObj.ticketed  =  dateTimeConvert(row[8])
            holcimDocketObj.load  =   dateTimeConvert(row[13])
            holcimDocketObj.loadComplete  = 0 if str(row[15]) == 'nan' else row[15]
            holcimDocketObj.toJob  =  dateTimeConvert(row[16])
            holcimDocketObj.timeToDepart  = 0 if str(row[18]) == 'nan' else row[18]
            holcimDocketObj.onJob  =  dateTimeConvert(row[19])
            holcimDocketObj.timeToSite  = 0 if str(row[21]) == 'nan' else row[21]
            holcimDocketObj.beginUnload  = dateTimeConvert(row[22])
            holcimDocketObj.waitingTime  = 0 if str(row[24]) == 'nan' else row[24]
            holcimDocketObj.endPour  = dateTimeConvert(row[25])
            holcimDocketObj.wash  =dateTimeConvert(row[26])
            holcimDocketObj.toPlant  =  dateTimeConvert(row[27])
            holcimDocketObj.timeOnSite  = 0 if str(row[32]) == 'nan' else row[32]
            holcimDocketObj.atPlant  =  dateTimeConvert(row[33])
            holcimDocketObj.leadDistance  = 0 if str(row[35]) == 'nan' else row[35]
            holcimDocketObj.returnDistance  = 0 if str(row[36]) == 'nan' else row[36]
            holcimDocketObj.totalDistance  = 0 if str(row[37]) == 'nan' else row[37]
            holcimDocketObj.totalTime  = 0 if str(row[38]) == 'nan' else row[38]
            holcimDocketObj.waitTimeBetweenJob  = 0 if str(row[39]) == 'nan' else row[39]
            holcimDocketObj.quantity  = 0 if str(row[41]) == 'nan' else row[41]
            holcimDocketObj.slump  = 0 if str(row[42]) == 'nan' else row[42]
            holcimDocketObj.waterAdded  = 0 if str(row[43]).strip() == 'nan' else str(row[43]).split('L')[0].strip()
            holcimDocketObj.save()
        except Exception as e:
            pastTripErrorObj = PastTripError(
                clientName = 'holcim',
                tripDate = tripDate,
                docketNumber = str(row[4]),
                truckNo = int(row[0]),
                lineNumber = count,
                errorFromPastTrip = e,
                fileName = secondaryFile.split('@_!')[-1],
                data = str(row),
                errorType = 1
            )
            pastTripErrorObj.save()

