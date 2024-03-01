from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
from Account_app.reconciliationUtils import  *
from datetime import time
import csv , re
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
    print(tripObj.id)
    docketQuerySet = DriverShiftDocket.objects.filter(tripId=tripObj.id)
    
    for docket in docketQuerySet:
        # print(docket.docketNumber , docket.shiftDate , docket.clientId , docket.truckConnectionId)
        reconciliationObj = ReconciliationReport.objects.filter(docketNumber = docket.docketNumber , docketDate = docket.shiftDate, clientId = docket.clientId, truckConnectionId = docket.truckConnectionId).first()
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

tripQuerySet = DriverShiftTrip.objects.filter(startDateTime__gte = '2024-01-01 00:00:00')
for trip in tripQuerySet:
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
                trip.revenueDeficit = thresholdDayShiftAmount - totalRevenue
                trip.save()
                print(trip.revenueDeficit)
                
        # exit()
    else:
        thresholdNightShiftObj = ThresholdNightShift.objects.filter(rate_card_name = rateCardObj ,start_date__lte = trip.startDateTime.date() , end_date__gte = trip.startDateTime.date()).first()
        thresholdNightShiftAmount = thresholdNightShiftObj.threshold_amount_per_day_shift
        res = getSelectedCostComponent(thresholdNightShiftObj)
        if thresholdNightShiftAmount > 0:
            res = getSelectedCostComponent(thresholdNightShiftObj)
            totalRevenue = calculateIncludedTripRevenue(trip,res)
            if totalRevenue <  thresholdNightShiftAmount:
                trip.revenueDeficit = thresholdNightShiftAmount - totalRevenue
                trip.save()
        # print(thresholdNightShiftAmount)
        # exit()
    # docketTotal = 