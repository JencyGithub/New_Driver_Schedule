from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
from Account_app.reconciliationUtils import  *
from datetime import time
import sys


f = open(r"scripts/addPastTripForMissingDriver.txt", 'r')
driverName = f.read()

matchingData = PastTripError.objects.filter(errorFromPastTrip="Driver matching query does not exist.", status=False)

for i in matchingData:
    try:
        data = i.data
        data = data.replace('[','').replace(']','').replace('\\n','').replace("'",'')
        data = data.split(',')
        

        pastDriver = data[4].strip().replace(' ','').lower()
        if ' ' in str(data[0].strip()):
            res_ = str(data[0].strip()).split()[0]
        elif '/' in str(data[0].strip()):
            str_ = str(data[0].strip()).split('/')
            res_ = str_[-1]+'-'+str_[-2]+'-'+str_[0]
        else:
            res_ = str(data[0].strip())


        shiftDate = datetime.strptime(res_, '%Y-%m-%d')

        startTime = datetime.strptime(str(data[6].strip()), '%H:%M:%S').time()
        startTimeDateTime = datetime.combine(shiftDate.date(), startTime)
        startTimeStr = startTimeDateTime.strftime('%Y-%m-%d %H:%M:%S')
        
        endTime = datetime.strptime(str(data[7].strip()), '%H:%M:%S').time()
        endTimeDateTime = datetime.combine(shiftDate.date(),endTime)
        endTimeStr =endTimeDateTime.strftime('%Y-%m-%d %H:%M:%S')
        clientObj = Client.objects.filter(name = i.clientName).first()
        
        driverObj = Driver.objects.filter(name = driverName).first()

        if pastDriver == driverName:
            i.status = True
            i.save()
            try:
                basePlant = BasePlant.objects.filter(basePlant = data[24].strip().upper()).first() 
                if basePlant is None:
                    pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "BasePlant does not exist.",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = "BasePlant does not exist.",
                            data = data
                        ) 
                    pastTripErrorObj.save()
                    continue
                
                clientTruckConnectionObj = ClientTruckConnection.objects.filter(clientTruckId = data[1].strip() , startDate__lte = shiftDate,endDate__gte = shiftDate, clientId = clientObj.clientId).first()
                if clientTruckConnectionObj is None:
                    pastTripErrorObj = PastTripError(
                        clientName = i.clientName,
                        tripDate = res_,
                        docketNumber = data[5],
                        truckNo = data[1],
                        lineNumber = i.lineNumber,
                        errorFromPastTrip = "Client truck connection object does not exist.",
                        fileName = i.fileName.split('@_!')[-1],
                        exceptionText ="Client truck connection object does not exist.",
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
                    
                    tripObj = DriverShiftTrip()
                    tripObj.verified = True
                    tripObj.shiftId = shiftId
                    tripObj.clientId = clientObj.clientId
                    
                    tripObj.truckConnectionId = clientTruckConnectionObj.id
                    
                    tripObj.save()

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

                    if tripObj.startDateTime and tripObj.endDateTime :

                        if tripObj.startDateTime.date() == startTimeDateTime.date() and tripObj.startDateTime.time() > startTimeDateTime.time():
                            tripObj.startDateTime = startTimeDateTime
                        if tripObj.endDateTime.date() == endTimeDateTime.date() and tripObj.endDateTime.time() < endTimeDateTime.time():
                            tripObj.endDateTime = endTimeDateTime
                            
                    else:
                        tripObj.startDateTime =startTimeDateTime
                        tripObj.endDateTime = endTimeDateTime
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
                
                                    
                shiftObj.endDateTime = tripObj.endDateTime
                shiftObj.save()
                tripObj.save()

                surCharge = Surcharge.objects.filter(surcharge_Name = 'No Surcharge').first()
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

                clientTruckConnectionObj = ClientTruckConnection.objects.filter(clientTruckId = data[1].strip() , startDate__lte = shiftDate,endDate__gte = shiftDate, clientId = clientObj.clientId).first()

                if clientTruckConnectionObj:
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
                            
                        
                        docketObj.basePlant = basePlant.id
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
        else:
            continue
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
    