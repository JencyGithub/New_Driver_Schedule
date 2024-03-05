from Account_app.reconciliationUtils import  *
from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
with open('last_subprocess_run_time.txt','w')as f:
    f.write('0')
f = open(r"scripts/updateTripsAndReconciliationData.txt", 'r')
data = f.read()
data = data.split(',')[0:-1]

reconciliationReportData = ReconciliationReport.objects.filter(docketDate__gte = data[1],docketDate__lte = data[2])

for obj in reconciliationReportData:

    try:
        if obj.fromDriver:
             # for ReconciliationReport 
            shiftObj = DriverShift.objects.filter(shiftDate = obj.docketDate , driverId = obj.driverId).first()
            clientObj = Client.objects.filter(pk=obj.clientId).first()
            clientTruckConnectionObj = ClientTruckConnection.objects.filter(pk=obj.truckConnectionId,startDate__lte = obj.docketDate,endDate__gte = obj.docketDate, clientId = clientObj).first()
            tripObj = DriverShiftTrip.objects.filter(shiftId = shiftObj.id , clientId = clientObj.clientId,truckConnectionId = clientTruckConnectionObj.id).first()
            docketObj = DriverShiftDocket.objects.filter(docketNumber = obj.docketNumber , tripId=tripObj.id , truckConnectionId = tripObj.truckConnectionId).first()
            rateCard = clientTruckConnectionObj.rate_card_name
            costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard.id,start_date__lte = docketObj.shiftDate,end_date__gte = docketObj.shiftDate).first()
            graceObj = Grace.objects.filter(rate_card_name = rateCard.id,start_date__lte = docketObj.shiftDate,end_date__gte = docketObj.shiftDate).first()
            
            if 'costParameters_loading_cost_per_cubic_meter' in data or 'costParameters_km_cost' in data or 'load_km_grace' in data or 'thresholdDayShift_min_load_in_cubic_meters' in data:
                obj.driverLoadAndKmCost = checkLoadAndKmCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)

            if 'costParameters_surcharge_type' in data or 'costParameters_surcharge_cost' in data:
                obj.driverSurchargeCost = checkSurcharge(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)

                
            obj.driverWaitingTimeCost = 0
            if 'costParameters_waiting_cost_per_minute' in data or 'waiting_time_grace_in_minutes' in data or 'chargeable_waiting_time_starts_after' in data or 'waiting_load_calculated_on_load_size ' in data or 'waiting_time_grace_per_cubic_meter ' in data or 'minimum_load_size_for_waiting_time_grace ' in data:
                if docketObj.waitingTimeStart and docketObj.waitingTimeEnd:
                    if graceObj.waiting_load_calculated_on_load_size:
                        obj.driverWaitingTimeCost = checkLoadCalculatedWaitingTime(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                    else:
                        obj.driverWaitingTimeCost = checkWaitingTime(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                
                
            if 'costParameters_transfer_cost' in data or 'transfer_km_grace' in data:
                obj.driverTransferKmCost = checkTransferCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                
            if 'return_km_grace' in data:
                obj.driverReturnKmCost = checkReturnCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
            
            obj.driverStandByCost = 0
            if 'costParameters_standby_cost_per_slot' in data or 'costParameters_standby_time_slot_size' in data or 'standby_time_grace_in_minutes' in data or 'chargeable_standby_time_starts_after' in data :
                if docketObj.standByStartTime and docketObj.standByEndTime:
                    slotSize = DriverTripCheckStandByTotal(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                    obj.driverStandByCost = checkStandByTotal(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                
                with open("scripts/updateTripsAndReconciliationDataError.txt", 'a') as f:
                    f.write(obj.docketNumber+','+'\n')
            
            if 'costParameters_loading_cost_per_cubic_meter' in data or 'costParameters_km_cost' in data or 'load_km_grace' in data or 'thresholdDayShift_min_load_in_cubic_meters' in data:
                obj.driverLoadDeficit = checkMinLoadCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                
            totalCost = obj.driverLoadAndKmCost + obj.driverSurchargeCost + obj.driverWaitingTimeCost   + obj.driverTransferKmCost + obj.driverReturnKmCost +obj.driverLoadDeficit  # + obj.driverStandByCost
            obj.driverTotalCost = round(totalCost,2)
            obj.save()
    except Exception as e:
        with open("scripts/updateTripsAndReconciliationDataError.txt", 'a') as f:
            f.write(str(e)+','+'\n')
            
            
with open('last_subprocess_run_time.txt','w')as f:
    f.write('1')