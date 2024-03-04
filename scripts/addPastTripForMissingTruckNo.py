from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
import pandas as pd
from Account_app.reconciliationUtils import  *
from datetime import time
import sys
from variables import *
from utils import *

f = open(r"scripts/addPastTripForMissingTruckNo.txt", 'r')
truckNo = f.read()
# data = data.split(',')[0:-1]

boralMatchingData = PastTripError.objects.filter(errorFromPastTrip="Client truck connection object does not exist.", status=False)
tripIdList = set()

for i in boralMatchingData:
    try:
        data = i.data
        data = data.replace('[','').replace(']','').replace('\\n','').replace("'",'')
        data = data.split(',')
        
        for j in range(len(data)):
            data[j] = data[j].strip()
            
        if ' ' in str(data[0]):
            res_ = str(data[0]).split()[0]
        elif '/' in str(data[0]):
            str_ = str(data[0]).split('/')
            year_ = '20'+str_[-1] if len(str_[-1]) == 2 else str_[-1]
            month_ = '0'+str_[-2] if len(str_[-2]) == 1 else str_[-2]
            res_ = year_+'-'+month_+'-'+str_[0]
        elif '-' in str(data[0]):
            str_ = str(data[0]).split('-')
            year_ = '20'+str_[-1] if len(str_[-1]) == 2 else str_[-1]
            month_ = '0'+str_[-2] if len(str_[-2]) == 1 else str_[-2]
            res_ = year_+'-'+month_+'-'+str_[0]
        else:
            res_ = str(data[0])


        shiftDate = datetime.strptime(res_, '%Y-%m-%d')
        clientObj = Client.objects.filter(name = i.clientName).first()
        clientTruckConnectionObj = ClientTruckConnection.objects.filter(clientTruckId = data[1].strip() , startDate__lte = shiftDate,endDate__gte = shiftDate, clientId = clientObj.clientId).first()
        # print(clientTruckConnectionObj)
        # exit()
        
        if clientTruckConnectionObj:
            i.status = True
            i.save()
            startTime = datetime.strptime(str(data[6]), '%H:%M:%S').time()
            startTimeDateTime = datetime.combine(shiftDate.date(), startTime)

            endTime = datetime.strptime(str(data[7]), '%H:%M:%S').time()
            endTimeDateTime = datetime.combine(shiftDate.date(),endTime)
            driverObj = Driver.objects.filter(driverId=int(data[4].strip())).first()
            tripObjGet = saveDate(driverObj = driverObj ,clientObj = clientObj ,data = data ,shiftDate = shiftDate ,startTimeDateTime =startTimeDateTime , endTimeDateTime = endTimeDateTime  , clientName_= i.clientName, fileName =i.fileName.split('@_!')[-1] ,res_ =res_,count_ =i.lineNumber)
            if tripObjGet:
                tripIdList.add(tripObjGet.id)


    except Exception as e:
        pastTripErrorObj = PastTripError(
            clientName = i.clientName,
            tripDate = res_,
            docketNumber = data[5],
            truckNo = data[1],
            lineNumber = i.lineNumber,
            errorFromPastTrip = e,
            fileName = i.fileName.split('@_!')[-1],
            exceptionText = e,
            data = data
        )
        pastTripErrorObj.save()
try:
    tripObjList = DriverShiftTrip.objects.filter(pk__in = tripIdList)
    checkShiftRevenueDifference(tripObjList=tripObjList)
except Exception as e:
    pass


















# def dateConvert(dataList,type_):
#     try:
#         if dataList.lower() != 'nan':
#             timestamp_obj = datetime.strptime(dataList, '%d/%m/%Y %I:%M:%S %p')
#             if type_ =='date':
#                 date_only_str = timestamp_obj.strftime('%Y-%m-%d')
#                 return date_only_str
#             elif type_ == 'time':
#                 time_only_str = timestamp_obj.strftime('%H:%M:%S')
#                 return time_only_str
#         else:
#             date_only_str = None  
#         return date_only_str
#     except Exception as e:
#         return None
    

# def dateTimeConvert(dataList):
#     try:
#         if pd.isna(dataList) or str(dataList).lower() == 'nan':
#             return None
#         else:
#             try:
#                 timestamp_obj = datetime.strptime(str(dataList),  '%Y-%m-%d %H:%M:%S')
#             except: 
#                 timestamp_obj = datetime.strptime(str(dataList), '%d/%m/%Y %I:%M:%S %p')
#             formatted_timestamp = timestamp_obj.strftime('%Y-%m-%d %H:%M:%S')
#             return formatted_timestamp
#     except ValueError as e:
#         return None
    
    
    
# holcimMatchingData = PastTripError.objects.filter(errorFromPastTrip="Client truck connection object does not exist.", status=False,clientName = 'holcim')

# if holcimMatchingData:
    # for i in holcimMatchingData:
        
        
    #     try:
    #         data = i.data
    #         data = data.replace('[','').replace(']','').replace('\\n','').replace("'",'')
    #         data = data.split(',')
            

    #         pastDriver = data[40].strip().replace(' ','').lower()
    #         driverId = Driver.objects.filter(name = pastDriver).first()
    #         pastTruckNo = data[0].strip().replace(' ','').lower()
    #         tripDate = dateConvert(str(data[8]).strip(),'date')
    #         client = Client.objects.filter(name = 'holcim').first()
    #         existingTrip = HolcimTrip.objects.filter(truckNo= pastTruckNo ,  shiftDate= tripDate).first()
    #         existingDockets = HolcimDocket.objects.filter(tripId = existingTrip.id).count()
    #         if pastTruckNo == truckNo:
    #             i.status =True
    #             i.save()
    #             try:
    #                 holcimDocketObj = HolcimDocket()
    #                 holcimDocketObj.truckNo  = pastTruckNo
    #                 holcimDocketObj.tripId  = existingTrip
    #                 holcimDocketObj.jobNo  =  data[4].strip()
    #                 if holcimDocketObj.jobNo == 'nan':
    #                     pastTripErrorObj = PastTripError(
    #                         clientName = 'holcim',
    #                         tripDate = tripDate,
    #                         docketNumber = str(data[4]),
    #                         truckNo = pastTruckNo,
    #                         lineNumber = i.lineNumber,
    #                         errorFromPastTrip = 'Job No. Missing.',
    #                         fileName = i.fileName.split('@_!')[-1],
    #                         data = data
    #                     )
    #                     pastTripErrorObj.save()
    #                     continue
    #                 holcimDocketObj.orderNo  = 0 if str(data[2]) == 'nan' else data[2].strip()
    #                 holcimDocketObj.status  = 0 if str(data[6]) == 'nan' else data[6].strip()
    #                 holcimDocketObj.ticketedDate  =  tripDate
    #                 holcimDocketObj.ticketedTime  =  dateConvert(str(data[8]).strip(),'time')
    #                 if holcimDocketObj.ticketedDate is None:
    #                     pastTripErrorObj = PastTripError(
    #                         clientName = 'holcim',
    #                         tripDate = tripDate,
    #                         docketNumber = str(data[4]),
    #                         truckNo = pastTruckNo,
    #                         lineNumber = i.lineNumber,
    #                         errorFromPastTrip = 'Ticketed Missing.',
    #                         fileName = i.fileName.split('@_!')[-1],
    #                         data = data
    #                     )
    #                     pastTripErrorObj.save()
    #                     continue
    #                 holcimDocketObj.load  =  dateTimeConvert(str(data[13]).strip())
    #                 holcimDocketObj.loadComplete  = 0 if str(data[15]).strip() == '' else data[15]
    #                 holcimDocketObj.toJob  =  dateTimeConvert(str(data[16]).strip())
    #                 holcimDocketObj.timeToDepart  = 0 if str(data[18]).strip() == '' else data[18]
    #                 holcimDocketObj.onJob  =  dateTimeConvert(str(data[19]).strip())
    #                 holcimDocketObj.timeToSite  = 0 if str(data[21]).strip() == '' else data[21]
    #                 holcimDocketObj.beginUnload  = dateTimeConvert(str(data[22]).strip())
    #                 holcimDocketObj.waitingTime  = 0 if str(data[24]).strip() == '' else data[24]
    #                 holcimDocketObj.endPour  = dateTimeConvert(str(data[25]).strip())
    #                 holcimDocketObj.wash  =dateTimeConvert(str(data[26]).strip())
    #                 holcimDocketObj.toPlant  =  dateTimeConvert(str(data[27]).strip())
    #                 holcimDocketObj.timeOnSite  = 0 if str(data[32]).strip() == '' else data[32]
    #                 holcimDocketObj.atPlant  =  dateTimeConvert(str(data[33]).strip())
    #                 holcimDocketObj.leadDistance  = 0 if str(data[35]).strip() == '' else data[35]
    #                 holcimDocketObj.returnDistance  = 0 if str(data[36]).strip() == '' else data[36]
    #                 holcimDocketObj.totalDistance  = 0 if str(data[37]).strip() == '' else data[37]
    #                 holcimDocketObj.totalTime  = 0 if str(data[38]).strip() == '' else data[38].strip()
    #                 holcimDocketObj.waitTimeBetweenJob  = 0 if str(data[39]).strip() == '' else data[39]
    #                 holcimDocketObj.driverName  = driverId #data[40]
    #                 holcimDocketObj.quantity  = 0 if str(data[41]).strip() == '' else data[41]
    #                 holcimDocketObj.slump  = 0 if str(data[42]).strip() == '' else data[42]
    #                 holcimDocketObj.waterAdded  = 0 if str(data[43]).strip() == '' else str(data[43]).replace('L','').strip()
    #                 holcimDocketObj.save()
    #                 existingTrip.numberOfLoads = existingDockets + 1
    #                 existingTrip.save()
                    
    #             except Exception as e:
    #                 print(e)
    #                 pastTripErrorObj = PastTripError(
    #                         clientName = 'holcim',
    #                         tripDate = tripDate,
    #                         docketNumber = str(data[4]),
    #                         truckNo = pastTruckNo,
    #                         lineNumber = i.lineNumber,
    #                         errorFromPastTrip = e,
    #                         fileName = i.fileName.split('@_!')[-1],
    #                         data = data
    #                     )
    #                 pastTripErrorObj.save()
    #     except Exception as e:
    #         print(e)
            
    #         pastTripErrorObj = PastTripError(
    #                 clientName = 'holcim',
    #                 tripDate = tripDate,
    #                 docketNumber = str(data[4]),
    #                 truckNo = pastTruckNo,
    #                 lineNumber = i.lineNumber,
    #                 errorFromPastTrip = e,
    #                 fileName = i.fileName.split('@_!')[-1],
    #                 data = data
    #             )
    #         pastTripErrorObj.save()