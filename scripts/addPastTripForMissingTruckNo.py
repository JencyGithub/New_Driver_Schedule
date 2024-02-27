from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
import pandas as pd
from Account_app.reconciliationUtils import  *
from datetime import time
import sys
from variables import *


f = open(r"scripts/addPastTripForMissingTruckNo.txt", 'r')
truckNo = f.read()
# data = data.split(',')[0:-1]

boralMatchingData = PastTripError.objects.filter(errorFromPastTrip="Client truck connection object does not exist.", status=False)

for i in boralMatchingData:
    try:
        data = i.data
        data = data.replace('[','').replace(']','').replace('\\n','').replace("'",'')
        data = data.split(',')
        

        if ' ' in str(data[0].strip()):
            res_ = str(data[0].strip()).split()[0]
        elif '/' in str(data[0].strip()):
            str_ = str(data[0].strip()).split('/')
            res_ = str_[-1]+'-'+str_[-2]+'-'+str_[0]
        else:
            res_ = str(data[0].strip())


        shiftDate = datetime.strptime(res_, '%Y-%m-%d')
        pastBasePlant = data[-1].strip().upper()
        pastDriver = data[4].strip().replace(' ','').lower()

        startTime = datetime.strptime(str(data[6].strip()), '%H:%M:%S').time()
        startTimeDateTime = datetime.combine(shiftDate.date(), startTime)
        startTimeStr = startTimeDateTime.strftime('%Y-%m-%d %H:%M:%S')
        
        endTime = datetime.strptime(str(data[7].strip()), '%H:%M:%S').time()
        endTimeDateTime = datetime.combine(shiftDate.date(),endTime)
        endTimeStr =endTimeDateTime.strftime('%Y-%m-%d %H:%M:%S')
        clientObj = Client.objects.filter(name = i.clientName).first()
        
        driverName = data[4].strip().replace(' ','').lower()
        driverObj = Driver.objects.filter(name = driverName).first()
        pastTruckNo = data[1].strip().replace(' ','').lower()
        
        basePlantObj = BasePlant.objects.filter(basePlant = pastBasePlant).first()
        clientTruckConnectionObj = ClientTruckConnection.objects.filter(clientTruckId = data[1].strip() , startDate__lte = shiftDate,endDate__gte = shiftDate, clientId = clientObj.clientId).first()
        
        if clientTruckConnectionObj:
            i.status = True
            i.save()
            
            try:
                # if clientTruckConnectionObj is None:
                #     pastTripErrorObj = PastTripError(
                #         clientName = i.clientName,
                #         tripDate = res_,
                #         docketNumber = data[5],
                #         truckNo = data[1],
                #         lineNumber = i.lineNumber,
                #         errorFromPastTrip = "Client truck connection object does not exist.",
                #         fileName = i.fileName.split('@_!')[-1],
                #         exceptionText ="Client truck connection object does not exist.",
                #         data = data
                #     )
                #     pastTripErrorObj.save()
                #     continue
                shiftObj = DriverShift.objects.filter(shiftDate = shiftDate , driverId = driverObj.driverId).first()
                if shiftObj is None:
                    shiftObj = DriverShift()
                    shiftObj.shiftDate =  shiftDate
                    shiftObj.driverId =  driverObj.driverId
                    shiftObj.shiftType = 'Day'
                    shiftObj.verified = True
                    shiftObj.save()
                    
                shiftId = shiftObj.id
                
                
                
                tripObj = DriverShiftTrip.objects.filter(shiftId = shiftId , truckConnectionId = clientTruckConnectionObj.id).first()
                if tripObj is None:
                    # print('Creating New Trip')
                    
                    tripObj = DriverShiftTrip()
                    tripObj.verified = True
                    tripObj.shiftId = shiftId
                    tripObj.clientId = clientObj.clientId
                    
                    tripObj.truckConnectionId = clientTruckConnectionObj.id
                    # print('truckConnection ',clientTruckConnectionObj,tripObj)
                    
                    tripObj.save()
                #     print('Trip Obj Created')
                # print('tripId',tripObj.id)

                # Docket save
                # existingDockets = DriverShiftDocket.objects.filter(tripId = tripObj.id,shiftId = shiftObj.id).count()
                # tripObj.numberOfLoads = existingDockets + 1
                
                shiftDate = datetime.strptime(res_, '%Y-%m-%d')

                try:
                    shiftDateStr = datetime.strftime(shiftDate.date(), '%Y-%m-%d')
                    
                    startTimeDateTime = shiftDateStr + ' ' + data[6].strip()                            
                    endTimeDateTime = shiftDateStr + ' ' + data[7].strip()
                    
                    startTimeDateTime = datetime.strptime(startTimeDateTime, '%Y-%m-%d %H:%M:%S')
                    endTimeDateTime = datetime.strptime(endTimeDateTime, '%Y-%m-%d %H:%M:%S')
                    
                    # print(startTimeDateTime, endTimeDateTime)
                except Exception as e:
                    pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "Incorrect date format",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = e,
                            data = data
                        ) 
                    pastTripErrorObj.save()
                    continue
                
                try:
                    # print(startTimeDateTime.tzinfo, startTimeDateTime)
                    # print(endTimeDateTime.tzinfo, endTimeDateTime)
                    if tripObj.startDateTime and tripObj.endDateTime :
                        # print('Start Date time Inside if')
                        # print(data[5], tripObj.startDateTime.date(),startTimeDateTime.date() , tripObj.startDateTime.time() , startTimeDateTime.time())
                        if tripObj.startDateTime.date() == startTimeDateTime.date() and tripObj.startDateTime.time() > startTimeDateTime.time():
                            tripObj.startDateTime = startTimeDateTime
                            # print('Updating Start Time trip match')
                        if tripObj.endDateTime.date() == endTimeDateTime.date() and tripObj.endDateTime.time() < endTimeDateTime.time():
                            tripObj.endDateTime = endTimeDateTime
                            # print('Updating End Time trip match')
                            
                    else:
                        # print('Start Date time Inside Else')
                        tripObj.startDateTime =startTimeDateTime
                        tripObj.endDateTime = endTimeDateTime
                        # print('Saved Start Time : ', startTimeDateTime ,  'Saved End Time' ,endTimeDateTime )
                except Exception as e:
                    pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "Incorrect date format",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = e,
                            data = data
                        ) 
                    pastTripErrorObj.save()
                    with open('IncorrectDate.txt','a') as f:
                        f.write(f'{e}\n')
                    continue
                
                shiftObj.startDateTime = tripObj.startDateTime
                
                # print('shift' , shiftObj.startDateTime)
                                    
                shiftObj.endDateTime = tripObj.endDateTime
                shiftObj.save()
                tripObj.save()

                surCharge = Surcharge.objects.filter(surcharge_Name = noSurcharge).first()
                docketObj = DriverShiftDocket.objects.filter(docketNumber = data[5].strip() , tripId=tripObj.id , truckConnectionId = tripObj.truckConnectionId).first()
                if docketObj :
                    pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "DocketNumber already Exist for this trip.",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = "DocketNumber already Exist for this trip.",
                            data = data
                        ) 
                    pastTripErrorObj.save()
                    continue
                docketObj = DriverShiftDocket()                
                # print('Docket Obj Created.')

                clientTruckConnectionObj = ClientTruckConnection.objects.filter(clientTruckId = data[1].strip() , startDate__lte = shiftDate,endDate__gte = shiftDate, clientId = clientObj.clientId).first()

                if clientTruckConnectionObj:
                    # print("finding ratecard")
                    rateCard = clientTruckConnectionObj.rate_card_name 
                    graceObj = Grace.objects.filter(rate_card_name = rateCard,start_date__lte = shiftObj.shiftDate,end_date__gte = shiftObj.shiftDate).first()

                    if not graceObj:
                        pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "No matching grace card for the date.",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = "No matching grace card for the date.",
                            data = data
                        ) 
                        # print('grace card not found')                   
                        pastTripErrorObj.save()
                        continue

                    costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard).first()

                    if not costParameterObj:
                        pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "No matching cost parameter card for the date.",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = "No matching cost parameter card for the date.",
                            data = data
                        )                    
                        pastTripErrorObj.save()
                        # print('COST PARAMETER not found')
                        continue
                        

                    try:
                        docketObj.shiftDate = shiftDate
                        docketObj.shiftId = shiftObj.id
                        docketObj.tripId = tripObj.id
                        docketObj.clientId = tripObj.clientId
                        docketObj.truckConnectionId = tripObj.truckConnectionId
                        docketObj.docketNumber = str(data[5].strip())
                        docketObj.noOfKm = 0 if str(data[10].strip()).lower() == '' else data[10].strip()
                        docketObj.transferKM = 0 if str(data[18].strip()).lower() == '' else data[18].strip()
                        docketObj.returnToYard = True if data[16].strip().lower() == 'yes' else False
                        docketObj.returnQty = 0 if str(data[14].strip()).lower() == '' else data[14].strip()
                        docketObj.returnKm = 0 if str(data[15].strip()).lower() == '' else data[15].strip()
                        docketObj.cubicMl = 0 if str(data[8].strip()).lower() == '' else data[8].strip()
                        docketObj.waitingTimeStart = None if str(data[11]).strip().lower() == '' else datetime.strptime(data[11].strip(), '%H:%M:%S').time()
                        docketObj.waitingTimeEnd = None if str(data[12]).strip().lower() == '' else datetime.strptime(data[12].strip(), '%H:%M:%S').time()
                        docketObj.standByStartTime = None if str(data[20].strip()).lower() == '' else datetime.strptime(data[20].strip(), '%H:%M:%S').time()
                        docketObj.standByEndTime = None if str(data[21].strip()).lower() == '' else datetime.strptime(data[21].strip(), '%H:%M:%S').time()
                        
                        # docketObj.standBySlot = standBySlot
                        docketObj.comment = data[17].strip()
                        # modification for adding blow back and replacement.
                        if data[19].strip().replace(' ','') != None:
                            docketObj.comment = docketObj.comment + 'Blow back comment : ' + data[19].strip() 
                            
                        if data[23].strip().replace(' ','') != None:
                            docketObj.comment = docketObj.comment + 'Replacement comment : ' + data[23].strip() 
                            
                        
                        docketObj.basePlant = basePlantObj.id
                        
                        docketObj.surcharge_type = surCharge.id

                        docketObj.save()
                    except Exception as e:
                        pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "Docket Save internal server error.",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = e,
                            data = data
                            )
                        pastTripErrorObj.save()
                        continue
                    try:
                        reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = docketObj.docketNumber, docketDate=docketObj.shiftDate , clientId = clientObj.clientId).first()
                        
                        if not  reconciliationDocketObj :
                            reconciliationDocketObj = ReconciliationReport()
                            
                            
                        reconciliationDocketObj.driverId = driverObj.driverId  
                        reconciliationDocketObj.clientId = clientObj.clientId
                        reconciliationDocketObj.truckConnectionId = tripObj.truckConnectionId
                        
                        # for ReconciliationReport 
                        clientTruckConnectionObj = ClientTruckConnection.objects.filter(pk=tripObj.truckConnectionId,startDate__lte = docketObj.shiftDate,endDate__gte = docketObj.shiftDate, clientId = clientObj).first()
                        rateCard = clientTruckConnectionObj.rate_card_name
                        costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard.id,start_date__lte = docketObj.shiftDate,end_date__gte = docketObj.shiftDate).first()
                        graceObj = Grace.objects.filter(rate_card_name = rateCard.id,start_date__lte = docketObj.shiftDate,end_date__gte = docketObj.shiftDate).first()
                        
                        driverLoadAndKmCost = checkLoadAndKmCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                        
                        driverSurchargeCost = checkSurcharge(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                        driverWaitingTimeCost = 0
                        driverStandByCost = 0
                        if docketObj.waitingTimeStart and docketObj.waitingTimeEnd:
                            if graceObj.waiting_load_calculated_on_load_size:
                                driverWaitingTimeCost = checkLoadCalculatedWaitingTime(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                            else:  
                                driverWaitingTimeCost = checkWaitingTime(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                        
                        if docketObj.standByStartTime and docketObj.standByEndTime:
                            slotSize = DriverTripCheckStandByTotal(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                            driverStandByCost = checkStandByTotal(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj,slotSize =slotSize)
                        driverTransferKmCost = checkTransferCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                        driverReturnKmCost = checkReturnCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                        # minLoad 
                        driverLoadDeficit = checkMinLoadCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                        # TotalCost 
                        driverTotalCost = driverLoadAndKmCost +driverSurchargeCost + driverWaitingTimeCost + driverStandByCost + driverTransferKmCost + driverReturnKmCost +driverLoadDeficit
                        reconciliationDocketObj.docketNumber = docketObj.docketNumber  
                        reconciliationDocketObj.docketDate = shiftObj.shiftDate 
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
                        # print("reconciliation done!!!!")
                    except Exception as e:
                        pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "Reconciliation Entry internal server error.",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = e,
                            data = data
                            )
                        pastTripErrorObj.save()
                        continue
                
                else:
                    pastTripErrorObj = PastTripError(
                        clientName = i.clientName,
                        tripDate = res_,
                        docketNumber = data[5],
                        truckNo = data[1],
                        lineNumber = i.lineNumber,
                        errorFromPastTrip = "Client truck connection object does not exist.",
                        fileName = i.fileName.split('@_!')[-1],
                        data = data
                    )
                    pastTripErrorObj.save()
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