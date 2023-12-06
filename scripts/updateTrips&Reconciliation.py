from Account_app.reconciliationUtils import  *
from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime

f = open(r"scripts/updateTrips&ReconciliationData.txt", 'r')
data = f.read()
data = data.split(',')[0:-1]

reconciliationReportData = ReconciliationReport.objects.filter(docketDate__gte = data[1],docketDate__lte = data[2])
# print(reconciliationReportData.docketNumber)

for obj in reconciliationReportData:
    if 'costParameters_loading_cost_per_cubic_meter' in data or 'costParameters_km_cost' in data or 'load_km_grace' in data or 'thresholdDayShift_min_load_in_cubic_meters' in data:
        obj.driverLoadAndKmCost = checkLoadAndKmCost(obj.docketNumber ,obj.docketDate)
        # print(obj.docketNumber,obj.driverLoadAndKmCost)

    if 'costParameters_surcharge_type' in data or 'costParameters_surcharge_cost' in data:
        obj.driverSurchargeCost = checkSurcharge(obj.docketNumber ,obj.docketDate)
        # print(obj.docketNumber,obj.driverLoadAndKmCost,obj.driverSurchargeCost)
        
        
    if 'costParameters_waiting_cost_per_minute' in data or 'waiting_time_grace_in_minutes' in data or 'chargeable_waiting_time_starts_after' in data:
        # print(obj.docketNumber,obj.driverWaitingTimeCost)
        obj.driverWaitingTimeCost = checkWaitingTime(obj.docketNumber ,obj.docketDate)
        # print(obj.docketNumber,obj.driverWaitingTimeCost)
        
    if 'costParameters_transfer_cost' in data or 'transfer_km_grace' in data:
        obj.driverTransferKmCost = checkTransferCost(obj.docketNumber ,obj.docketDate)
        # print(obj.docketNumber,obj.driverTransferKmCost)
        
    if 'return_km_grace' in data:
        obj.driverReturnKmCost = checkReturnCost(obj.docketNumber ,obj.docketDate)
        # print(obj.docketNumber,obj.driverReturnKmCost)
        
    # if 'costParameters_standby_cost_per_slot' in data:
    #     obj.driverStandByCost = checkStandByTotal(obj.docketNumber ,obj.docketDate)
        # print(obj.docketNumber,obj.driverStandByCost)
        
    if 'costParameters_loading_cost_per_cubic_meter' in data or 'costParameters_km_cost' in data or 'load_km_grace' in data or 'thresholdDayShift_min_load_in_cubic_meters' in data:
        obj.driverLoadDeficit = checkMinLoadCost(obj.docketNumber ,obj.docketDate)
        # print(obj.docketNumber,obj.driverLoadDeficit)
    totalCost = obj.driverLoadAndKmCost + obj.driverSurchargeCost + obj.driverWaitingTimeCost   + obj.driverTransferKmCost + obj.driverReturnKmCost +obj.driverLoadDeficit  # + obj.driverStandByCost
    obj.driverTotalCost = round(totalCost,2)
    obj.save()