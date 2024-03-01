from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
from Account_app.reconciliationUtils import  *
from datetime import time
import warnings
from variables import *


reconciliationQuerySet = ReconciliationReport.objects.filter(fromDriver = True)

for reconciliationDocketObj in reconciliationQuerySet:
    docketObj = DriverShiftDocket.objects.filter(docketNumber = reconciliationDocketObj.docketNumber ,shiftDate =  reconciliationDocketObj.docketDate , clientId = reconciliationDocketObj.clientId ,truckConnectionId =reconciliationDocketObj.truckConnectionId).first()
    tripObj = DriverShiftTrip.objects.filter(pk=docketObj.tripId).first()
    shiftObj = DriverShift.objects.filter(pk=docketObj.shiftId).first()
    clientObj = Client.objects.filter(clientId = docketObj.clientId).first()
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
    checkMissingComponents(reconciliationDocketObj)
    # print('Save' , reconciliationDocketObj.docketNumber , reconciliationDocketObj.driverWaitingTimeCost , reconciliationDocketObj.missingComponent)