# import pandas as pd
from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
from Account_app.reconciliationUtils import  *
from datetime import time
import warnings
from variables import *

def run():
    warnings.filterwarnings('ignore')
    f = open(r"pastTrip_entry.txt", 'r')
    data = f.read().split(',')
    file_name = data[0]
    clientName_ = data[1]
    # res_ = None
    
    monthFileName = open(r"pastTrip_entry_month.txt",'r')
    monthAndYear = monthFileName.read()

    fileName = f'static/Account/PastTripsEntry/{file_name}'
    # fileName = f'static/Account/PastTripsEntry/20240121134630@_!01JanData1-152023.xlsx-Pasttrip.csv'

    txtFile = open(r'static/subprocessFiles/errorFromPastTrip.txt','w')
    txtFile.write(f'File:{file_name}\n\n')
    txtFile.close()

    with open(fileName, 'r') as pastData:
        count = 0
        for line in pastData:
            res_ = ''
            if ' ' in str(data[0]):
                res_ = str(data[0]).split()[0]
            elif '/' in str(data[0]):
                str_ = str(data[0]).split('/')
                res_ = str_[-1]+'-'+str_[-2]+'-'+str_[0]
            else:
                res_ = str(data[0])
            try:
                if '"' in line:
                   line = str(line).replace('"','')
                if "'" in line:
                   line =  str(line).replace("'","")
                count += 1
                if count == 1:
                    continue
                # if count == 10:
                #     exit() 
                data = line.split(',')

                if len(data) != 25:
                    pastTripErrorObj = PastTripError(
                                    clientName = clientName_,
                                    tripDate = res_,
                                    docketNumber = data[5],
                                    truckNo = data[1],
                                    lineNumber = count,
                                    errorFromPastTrip = "File Data in wrong format.",
                                    fileName = fileName.split('@_!')[-1],
                                    exceptionText = "File Data in wrong format.",
                                    data = data
                                )                    
                    pastTripErrorObj.save()
                    continue
                
                        
                
                if ' ' in str(data[0]):
                    res_ = str(data[0]).split()[0]
                elif '/' in str(data[0]):
                    str_ = str(data[0]).split('/')
                    res_ = str_[-1]+'-'+str_[-2]+'-'+str_[0]
                else:
                    res_ = str(data[0])

                # with open(r'pastDataRow.txt','a') as f:
                #     f.write(str(data[0]) + '\n')
                # print(count)
                shiftDate = datetime.strptime(res_, '%Y-%m-%d')
                # print('-----------------------------------------')
                # print('shiftDate',shiftDate , type(shiftDate))
                # print('-----------------------------------------')
                startTime = datetime.strptime(str(data[6]), '%H:%M:%S').time()
                startTimeDateTime = datetime.combine(shiftDate.date(), startTime)
                startTimeStr = startTimeDateTime.strftime('%Y-%m-%d %H:%M:%S')
                # print(getMaxTimeFromTwoTime(str(startTimeStr),startTimeStr,'min'))
                
                endTime = datetime.strptime(str(data[7]), '%H:%M:%S').time()
                endTimeDateTime = datetime.combine(shiftDate.date(),endTime)
                endTimeStr =endTimeDateTime.strftime('%Y-%m-%d %H:%M:%S')
                # print('shiftDate',data[6],data[7])

                if res_.split('-')[1] != monthAndYear.split('-')[-1] or res_.split('-')[0] != monthAndYear.split('-')[0]:
                    pastTripErrorObj = PastTripError(
                                clientName = clientName_,
                                tripDate = res_,
                                docketNumber = data[5],
                                truckNo = data[1],
                                lineNumber = count,
                                errorFromPastTrip = "Incorrect month/year values present in file.",
                                fileName = fileName.split('@_!')[-1],
                                exceptionText = "Incorrect month/year values present in file.",
                                
                                data = data
                            ) 
                            # print('grace card not found')                   
                    pastTripErrorObj.save()
                    continue
                    

                driverName = data[4].strip().replace(' ','').lower()
                clientObj = Client.objects.filter(name = clientName_).first()
                
                driverObj = Driver.objects.filter(name = driverName).first()
                
                if driverObj:
                    
                    # Trip save
                    try:
                        basePlant = BasePlant.objects.filter(basePlant = data[24].strip().upper()).first() 
                        if basePlant is None:
                            pastTripErrorObj = PastTripError(
                                    clientName = clientName_,
                                    tripDate = res_,
                                    docketNumber = data[5],
                                    truckNo = data[1],
                                    lineNumber = count,
                                    errorFromPastTrip = "BasePlant does not exist.",
                                    fileName = fileName.split('@_!')[-1],
                                    exceptionText = "BasePlant does not exist.",
                                    data = data
                                ) 
                            pastTripErrorObj.save()
                            continue
                        clientTruckConnectionObj = ClientTruckConnection.objects.filter(clientTruckId = data[1] , startDate__lte = shiftDate,endDate__gte = shiftDate, clientId = clientObj.clientId).first()
                        if clientTruckConnectionObj is None:
                            pastTripErrorObj = PastTripError(
                                clientName = clientName_,
                                tripDate = res_,
                                docketNumber = data[5],
                                truckNo = data[1],
                                lineNumber = count,
                                errorFromPastTrip = "Client truck connection object does not exist.",
                                fileName = fileName.split('@_!')[-1],
                                exceptionText = "Client truck connection object does not exist.",
                                
                                data = data
                            )
                            pastTripErrorObj.save()
                            continue
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
                                    clientName = clientName_,
                                    tripDate = res_,
                                    docketNumber = data[5],
                                    truckNo = data[1],
                                    lineNumber = count,
                                    errorFromPastTrip = "Incorrect date format",
                                    fileName = fileName.split('@_!')[-1],
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
                                    clientName = clientName_,
                                    tripDate = res_,
                                    docketNumber = data[5],
                                    truckNo = data[1],
                                    lineNumber = count,
                                    errorFromPastTrip = "Incorrect date format",
                                    fileName = fileName.split('@_!')[-1],
                                    exceptionText = e,
                                    data = data
                                ) 
                            pastTripErrorObj.save()
                            continue
                        
                        shiftObj.startDateTime = tripObj.startDateTime
                        
                        # print('shift' , shiftObj.startDateTime)
                                         
                        shiftObj.endDateTime = tripObj.endDateTime
                        shiftObj.save()
                        tripObj.save()
                        # print('startDateTime Set' , tripObj.startDateTime)
                        # print('EndDateTime Set' , tripObj.endDateTime)

                        surCharge = Surcharge.objects.filter(surcharge_Name = noSurcharge).first()
                        docketObj = DriverShiftDocket.objects.filter(docketNumber = data[5].strip() , tripId=tripObj.id , truckConnectionId = tripObj.truckConnectionId).first()
                        if docketObj :
                            pastTripErrorObj = PastTripError(
                                    clientName = clientName_,
                                    tripDate = res_,
                                    docketNumber = data[5],
                                    truckNo = data[1],
                                    lineNumber = count,
                                    errorFromPastTrip = "DocketNumber already Exist for this trip.",
                                    fileName = fileName.split('@_!')[-1],
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
                                    clientName = clientName_,
                                    tripDate = res_,
                                    docketNumber = data[5],
                                    truckNo = data[1],
                                    lineNumber = count,
                                    errorFromPastTrip = "No matching grace card for the date.",
                                    fileName = fileName.split('@_!')[-1],
                                    exceptionText = "No matching grace card for the date.",
                                    
                                    data = data
                                ) 
                                # print('grace card not found')                   
                                pastTripErrorObj.save()
                                continue

                            costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard).first()

                            if not costParameterObj:
                                pastTripErrorObj = PastTripError(
                                    clientName = clientName_,
                                    tripDate = res_,
                                    docketNumber = data[5],
                                    truckNo = data[1],
                                    lineNumber = count,
                                    errorFromPastTrip = "No matching cost parameter card for the date.",
                                    fileName = fileName.split('@_!')[-1],
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
                                docketObj.docketNumber = data[5]
                                docketObj.noOfKm = 0 if str(data[10]).lower() == '' else data[10]
                                docketObj.transferKM = 0 if str(data[18]).lower() == '' else data[18]
                                docketObj.returnToYard = True if data[16].lower() == 'yes' else False
                                docketObj.returnQty = 0 if str(data[14]).lower() == '' else data[14]
                                docketObj.returnKm = 0 if str(data[15]).lower() == '' else data[15]
                                docketObj.cubicMl = 0 if str(data[8]).lower() == '' else data[8]
                                waitingTimeStart = None if str(data[11]).strip().lower() == '' else str(data[11]).strip().lower()
                                waitingTimeEnd = None if str(data[12]).strip().lower() == '' else str(data[12]).strip().lower()

                                waitingTimeStartCount = 0 
                                waitingTimeEndCount = 0
                                if waitingTimeStart != None:
                                    waitingTimeStartCount = waitingTimeStart.count(':')
                                if waitingTimeEnd != None:
                                    waitingTimeEndCount = waitingTimeEnd.count(':')

                                if waitingTimeStart is not None and waitingTimeStartCount == 1:
                                    waitingTimeStart = str(datetime.strptime(data[11].strip(), '%H:%M').time())
                                elif waitingTimeStartCount == 2:
                                    waitingTimeStart = str(datetime.strptime(data[11].strip(), '%H:%M:%S').time())
                                if waitingTimeEnd is not None and waitingTimeEndCount == 1:
                                    waitingTimeEnd = str(datetime.strptime(data[12].strip(), '%H:%M').time())
                                elif waitingTimeEndCount == 2:
                                    waitingTimeEnd = str(datetime.strptime(data[12].strip(), '%H:%M:%S').time())
                                docketObj.waitingTimeStart = waitingTimeStart
                                docketObj.waitingTimeEnd = waitingTimeEnd
                                # docketObj.totalWaitingInMinute = totalWaitingTime
                                standByStartTime = None if str(data[20]).strip().lower() == '' else str(data[20]).strip().lower()
                                standByEndTime = None if str(data[21]).strip().lower() == '' else str(data[21]).strip().lower()

                                # Initialize counts to 0
                                standByStartCount = 0 
                                standByEndCount = 0
                                if standByStartTime != None:
                                    standByStartCount = standByStartTime.count(':')
                                if standByEndTime != None:
                                    standByEndCount = standByEndTime.count(':')

                                if standByStartCount == 1 and standByStartTime is not None:
                                    standByStartTime = str(datetime.strptime(data[20].strip(), '%H:%M').time())
                                elif standByStartCount == 2:
                                    standByStartTime = str(datetime.strptime(data[20].strip(), '%H:%M:%S').time())
                                    
                                if standByEndCount == 1 and standByEndTime is not None:
                                    standByEndTime = str(datetime.strptime(data[21].strip(), '%H:%M').time())
                                elif standByEndCount == 2:
                                    standByEndTime = str(datetime.strptime(data[21].strip(), '%H:%M:%S').time())

                                docketObj.standByStartTime = standByStartTime
                                docketObj.standByEndTime = standByEndTime
                                docketObj.comment = data[17]
                                # modification for adding blow back and replacement.
                                if data[19].strip().replace(' ','') != None:
                                    docketObj.comment = docketObj.comment + 'Blow back comment : ' + data[19].strip() 
                                    
                                if data[23].strip().replace(' ','') != None:
                                    docketObj.comment = docketObj.comment + 'Replacement comment : ' + data[23].strip() 
                                    
                                
                                docketObj.basePlant = basePlant.id
                                docketObj.surcharge_type = surCharge.id
                                # surcharge_duration = 
                                # others = 
                                docketObj.save()
                            except Exception as e:
                                pastTripErrorObj = PastTripError(
                                    clientName = clientName_,
                                    tripDate = res_,
                                    docketNumber = data[5],
                                    truckNo = data[1],
                                    lineNumber = count,
                                    errorFromPastTrip = "Docket Save internal server error.",
                                    fileName = fileName.split('@_!')[-1],
                                    exceptionText = e,
                                    data = data
                                    )
                                pastTripErrorObj.save()
                                # print('Docket save Error:', e)
                                continue
                            # print('Docket obj saved')
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

                                driverWaitingTimeCost =0
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
                                    clientName = clientName_,
                                    tripDate = res_,
                                    docketNumber = data[5],
                                    truckNo = data[1],
                                    lineNumber = count,
                                    errorFromPastTrip = "Reconciliation Entry internal server error.",
                                    fileName = fileName.split('@_!')[-1],
                                    exceptionText =e,
                                    data = data
                                    )
                                pastTripErrorObj.save()
                                continue
                        
                        else:
                            pastTripErrorObj = PastTripError(
                                clientName = clientName_,
                                tripDate = res_,
                                docketNumber = data[5],
                                truckNo = data[1],
                                lineNumber = count,
                                errorFromPastTrip = "Client truck connection object does not exist.",
                                fileName = fileName.split('@_!')[-1],
                                exceptionText ="Client truck connection object does not exist.",
                                
                                data = data
                            )
                            pastTripErrorObj.save()
                    except Exception as e:       
                        pastTripErrorObj = PastTripError(
                            clientName = clientName_,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = count,
                            errorFromPastTrip = e,
                            fileName = fileName.split('@_!')[-1],
                            exceptionText = e,
                            data = data
                        )
                        pastTripErrorObj.save()
                else:
                    pastTripErrorObj = PastTripError(
                            clientName = clientName_,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = count,
                            errorFromPastTrip = 'Driver matching query does not exist.',
                            fileName = fileName.split('@_!')[-1],
                            exceptionText = 'Driver matching query does not exist.',
                            data = data
                        )
                    pastTripErrorObj.save()
                    
                    
            except Exception as e:
                pastTripErrorObj = PastTripError(
                        clientName = clientName_,
                        tripDate = res_,
                        docketNumber = data[5],
                        truckNo = data[1],
                        lineNumber = count,
                        errorFromPastTrip = e,
                        fileName = fileName.split('@_!')[-1],
                        exceptionText = e,
                        data = data
                    )
                pastTripErrorObj.save()
                
