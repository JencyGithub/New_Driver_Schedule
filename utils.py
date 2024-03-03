# import pandas as pd
from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
from Account_app.reconciliationUtils import  *
from datetime import time
import warnings
from variables import *
def getSelectedCostComponent(obj):
    checked = []
    
    checked.append('loading_cost_per_cubic_meter_included') if obj.loading_cost_per_cubic_meter_included else None
    checked.append('km_cost_included') if obj.km_cost_included else None
    checked.append('surcharge_included') if obj.surcharge_included else None
    checked.append('transfer_cost_included') if obj.transfer_cost_included else None
    checked.append('return_cost_included') if obj.return_cost_included else None
    checked.append('standby_cost_included') if obj.standby_cost_included else None
    checked.append('waiting_cost_included') if obj.waiting_cost_included else None
    checked.append('call_out_fees_included') if obj.call_out_fees_included else None
        
    return checked  
    
def calculateIncludedTripRevenue(tripObj,checkedList:list):
    total=0
    docketQuerySet = DriverShiftDocket.objects.filter(tripId=tripObj.id)
    for docket in docketQuerySet:
        # print(docket.docketNumber , docket.shiftDate , docket.clientId , docket.truckConnectionId)
        reconciliationObj = ReconciliationReport.objects.filter(docketNumber = docket.docketNumber , docketDate = docket.shiftDate, clientId = docket.clientId).first()
        # print('reconciliationObj',reconciliationObj)
        # print(reconciliationObj)
        # exit()
        total += (float(reconciliationObj.driverLoadAndKmCost) + float(reconciliationObj.driverLoadDeficit))if 'loading_cost_per_cubic_meter_included' in checkedList else 0
        # total += float(reconciliationObj.driverLoadAndKmCost) if 'km_cost_included' in checkedList else 0
        total += float(reconciliationObj.driverSurchargeCost) if 'surcharge_included' in checkedList else 0
        total += float(reconciliationObj.driverTransferKmCost)  if 'transfer_cost_included' in checkedList else 0
        total += float(reconciliationObj.driverReturnKmCost) if 'return_cost_included' in checkedList else 0
        total += float(reconciliationObj.driverStandByCost) if 'standby_cost_included' in checkedList else 0
        total += float(reconciliationObj.driverWaitingTimeCost) if 'waiting_cost_included' in checkedList else 0
        total += float(reconciliationObj.driverCallOut) if 'call_out_fees_included' in checkedList else 0
    return total

def checkShiftRevenueDifference(tripObjList): 
    for trip in tripObjList:
        shiftObj = DriverShift.objects.filter(pk=trip.shiftId).first()
        shiftType = shiftObj.shiftType
        clientTruckConnectionObj = ClientTruckConnection.objects.filter(pk=trip.truckConnectionId).first()
        rateCardObj = clientTruckConnectionObj.rate_card_name
        if shiftType == 'Day':
            thresholdDayShiftObj = ThresholdDayShift.objects.filter(rate_card_name = rateCardObj ,start_date__lte = trip.startDateTime.date() , end_date__gte = trip.startDateTime.date()).first()
            thresholdDayShiftAmount = thresholdDayShiftObj.threshold_amount_per_day_shift
            if thresholdDayShiftAmount > 0:
                res = getSelectedCostComponent(thresholdDayShiftObj)
                totalRevenue = calculateIncludedTripRevenue(trip,res)
                if totalRevenue <  thresholdDayShiftAmount:
                    trip.revenueDeficit = round((thresholdDayShiftAmount - totalRevenue),2)
                    trip.save()
                    
            # exit()
        else:
            thresholdNightShiftObj = ThresholdNightShift.objects.filter(rate_card_name = rateCardObj ,start_date__lte = trip.startDateTime.date() , end_date__gte = trip.startDateTime.date()).first()
            thresholdNightShiftAmount = thresholdNightShiftObj.threshold_amount_per_day_shift
            res = getSelectedCostComponent(thresholdNightShiftObj)
            if thresholdNightShiftAmount > 0:
                res = getSelectedCostComponent(thresholdNightShiftObj)
                totalRevenue = calculateIncludedTripRevenue(trip,res)
                if totalRevenue <  thresholdNightShiftAmount:
                    trip.revenueDeficit = round((thresholdNightShiftAmount - totalRevenue),2)
                    trip.save()
          
def saveDate(driverObj,clientObj,data,shiftDate,startTimeDateTime,endTimeDateTime , clientName_, fileName ,res_,count_):  
    if not driverObj:
        pastTripErrorObj = PastTripError(
                clientName = clientName_,
                tripDate = res_,
                docketNumber = data[5],
                truckNo = data[1],
                lineNumber = count_,
                errorFromPastTrip = 'Driver matching query does not exist.',
                fileName = fileName.split('@_!')[-1],
                exceptionText = 'Driver matching query does not exist.',
                data = data
            )
        pastTripErrorObj.save()
        return 
    try:
        basePlant = BasePlant.objects.filter(basePlant = data[24].strip().upper()).first() 
        if basePlant is None:
            pastTripErrorObj = PastTripError(
                    clientName = clientName_,
                    tripDate = res_,
                    docketNumber = data[5],
                    truckNo = data[1],
                    lineNumber = count_,
                    errorFromPastTrip = "BasePlant does not exist.",
                    fileName = fileName.split('@_!')[-1],
                    exceptionText = "BasePlant does not exist.",
                    data = data
                ) 
            pastTripErrorObj.save()
            return
        clientTruckConnectionObj = ClientTruckConnection.objects.filter(clientTruckId = data[1] , startDate__lte = shiftDate,endDate__gte = shiftDate, clientId = clientObj.clientId).first()
        if clientTruckConnectionObj is None:
            pastTripErrorObj = PastTripError(
                clientName = clientName_,
                tripDate = res_,
                docketNumber = data[5],
                truckNo = data[1],
                lineNumber = count_,
                errorFromPastTrip = "Client truck connection object does not exist.",
                fileName = fileName.split('@_!')[-1],
                exceptionText = "Client truck connection object does not exist.",
                
                data = data
            )
            pastTripErrorObj.save()
            return
        shiftObj = DriverShift.objects.filter(shiftDate = shiftDate , driverId = driverObj.driverId).first()
        if shiftObj is None:
            shiftObj = DriverShift()
            shiftObj.shiftDate =  shiftDate
            shiftObj.driverId =  driverObj.driverId
            shiftObj.shiftType = 'Day' if data[25].strip().lower() == 'day' else  'Night'
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
        # print('DriverObj',driverObj)
        
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
                    lineNumber = count_,
                    errorFromPastTrip = "Incorrect date format",
                    fileName = fileName.split('@_!')[-1],
                    exceptionText = e,
                    data = data
                ) 
            pastTripErrorObj.save()
            return
        
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
                    clientName = clientName_,
                    tripDate = res_,
                    docketNumber = data[5],
                    truckNo = data[1],
                    lineNumber = count_,
                    errorFromPastTrip = "Incorrect date format",
                    fileName = fileName.split('@_!')[-1],
                    exceptionText = e,
                    data = data
                ) 
            pastTripErrorObj.save()
            return
        
        shiftObj.startDateTime = tripObj.startDateTime
        shiftObj.endDateTime = tripObj.endDateTime
        shiftObj.save()
        # existingDockets = DriverShiftDocket.objects.filter(tripId = tripObj.id,shiftId = shiftObj.id).count()
        # print(' BeforeTripObj', tripObj.id ,  tripObj.numberOfLoads)
        tripObj.numberOfLoads  += 1
        tripObj.save()
        
        # print(' AfterTripObj', tripObj.id  , tripObj.numberOfLoads)
            

        surCharge = Surcharge.objects.filter(surcharge_Name = noSurcharge).first()
        docketObj = DriverShiftDocket.objects.filter(docketNumber = data[5].strip() , tripId=tripObj.id , truckConnectionId = tripObj.truckConnectionId).first()
        if docketObj :
            pastTripErrorObj = PastTripError(
                    clientName = clientName_,
                    tripDate = res_,
                    docketNumber = data[5],
                    truckNo = data[1],
                    lineNumber = count_,
                    errorFromPastTrip = "DocketNumber already Exist for this trip.",
                    fileName = fileName.split('@_!')[-1],
                    exceptionText = "DocketNumber already Exist for this trip.",
                    data = data
                ) 
            pastTripErrorObj.save()
            return
        docketObj = DriverShiftDocket()                

        clientTruckConnectionObj = ClientTruckConnection.objects.filter(clientTruckId = data[1].strip() , startDate__lte = shiftDate,endDate__gte = shiftDate, clientId = clientObj.clientId).first()
        if not clientTruckConnectionObj:
            pastTripErrorObj = PastTripError(
                clientName = clientName_,
                tripDate = res_,
                docketNumber = data[5],
                truckNo = data[1],
                lineNumber = count_,
                errorFromPastTrip = "Client truck connection object does not exist.",
                fileName = fileName.split('@_!')[-1],
                exceptionText ="Client truck connection object does not exist.",
                
                data = data
            )
            pastTripErrorObj.save()
            return
        
        rateCard = clientTruckConnectionObj.rate_card_name 
        graceObj = Grace.objects.filter(rate_card_name = rateCard,start_date__lte = shiftObj.shiftDate,end_date__gte = shiftObj.shiftDate).first()

        if not graceObj:
            pastTripErrorObj = PastTripError(
                clientName = clientName_,
                tripDate = res_,
                docketNumber = data[5],
                truckNo = data[1],
                lineNumber = count_,
                errorFromPastTrip = "No matching grace card for the date.",
                fileName = fileName.split('@_!')[-1],
                exceptionText = "No matching grace card for the date.",
                
                data = data
            ) 
            # print('grace card not found')                   
            pastTripErrorObj.save()
            return

        costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard).first()
        if not costParameterObj:
            pastTripErrorObj = PastTripError(
                clientName = clientName_,
                tripDate = res_,
                docketNumber = data[5],
                truckNo = data[1],
                lineNumber = count_,
                errorFromPastTrip = "No matching cost parameter card for the date.",
                fileName = fileName.split('@_!')[-1],
                exceptionText = "No matching cost parameter card for the date.",
                
                data = data
            )                    
            pastTripErrorObj.save()
            # print('COST PARAMETER not found')
            return
            
        
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

            # Initialize Counts to 0
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
                lineNumber = count_,
                errorFromPastTrip = "Docket Save internal server error.",
                fileName = fileName.split('@_!')[-1],
                exceptionText = e,
                data = data
                )
            pastTripErrorObj.save()
            return
        
        try:
            reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = docketObj.docketNumber, docketDate=docketObj.shiftDate , clientId = clientObj.clientId, truckConnectionId = docketObj.truckConnectionId).first()
            
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
            
            minimumLoadIncludedFlag = False if data[28].strip().lower() == 'no' else True
            driverLoadAndKmCost = checkLoadAndKmCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj, minimumLoadIncluded = minimumLoadIncludedFlag)
            
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
            driverLoadDeficit = 0
            if minimumLoadIncludedFlag:
                driverLoadDeficit = checkMinLoadCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
            
            callOutFees =  costParameterObj.call_out_fees if data[29].strip().lower() == 'yes' else 0
            cancellationFees =  costParameterObj.cancellation_fees if data[29].strip().lower() == 'yes' else 0
            demurrageFees =  costParameterObj.demurrage_fees if data[29].strip().lower() == 'yes' else 0
            # TotalCost 
            driverTotalCost = driverLoadAndKmCost +driverSurchargeCost + driverWaitingTimeCost + driverStandByCost + driverTransferKmCost + driverReturnKmCost +driverLoadDeficit + callOutFees+cancellationFees + demurrageFees
            
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
            reconciliationDocketObj.driverCallOut = callOutFees
            reconciliationDocketObj.driverCancellationCost = cancellationFees
            reconciliationDocketObj.driverDemurageCost = demurrageFees
            reconciliationDocketObj.save()
            checkMissingComponents(reconciliationDocketObj)
            return tripObj
            # print("reconciliation done!!!!")
        except Exception as e:
            pastTripErrorObj = PastTripError(
                clientName = clientName_,
                tripDate = res_,
                docketNumber = data[5],
                truckNo = data[1],
                lineNumber = count_,
                errorFromPastTrip = "Reconciliation Entry internal server error.",
                fileName = fileName.split('@_!')[-1],
                exceptionText =e,
                data = data
                )
            pastTripErrorObj.save()
            return
    except Exception as e:       
        pastTripErrorObj = PastTripError(
            clientName = clientName_,
            tripDate = res_,
            docketNumber = data[5],
            truckNo = data[1],
            lineNumber = count_,
            errorFromPastTrip = e,
            fileName = fileName.split('@_!')[-1],
            exceptionText = e,
            data = data
        )
        pastTripErrorObj.save()

