from Account_app.models import *
from GearBox_app.models import *
from django.utils import timezone 
import datetime
from django.shortcuts import get_object_or_404
from CRUD import *
from datetime import datetime

costDict = {
    'rctiCosts': {
        'loadAndKmCost':0,
        'surchargeCost':0,
        'waitingTimeCost':0,
        'standByTotalCost':0        
    },
    'driverDocketCosts':{
        'loadAndKmCost':0,
        'surchargeCost':0,
        'waitingTimeCost':0,
        'standByTotalCost':0
    }
}
def DriverTripCheckWaitingTime(docketObj , shiftObj , rateCard , costParameterObj , graceObj):
    date_= docketObj.shiftDate
       
    totalWaitingTime = timeDifference(docketObj.waitingTimeStart,docketObj.waitingTimeEnd)
    
    if float(totalWaitingTime) > graceObj.chargeable_waiting_time_starts_after:
        totalWaitingTime = totalWaitingTime - graceObj.waiting_time_grace_in_minutes
        if totalWaitingTime < 0:
            totalWaitingTime = 0    
    else:
        totalWaitingTime = 0
    return totalWaitingTime
    
def DriverTripCheckStandByTotal(docketObj , shiftObj , rateCard , costParameterObj , graceObj):


    totalStandByTime = getTimeDifference(docketObj.standByStartTime,docketObj.standByEndTime)
    standBySlot = 0
    if totalStandByTime > graceObj.chargeable_standby_time_starts_after:
        totalStandByTime = totalStandByTime - graceObj.standby_time_grace_in_minutes
        standBySlot = totalStandByTime//costParameterObj.standby_time_slot_size
    return standBySlot
    
def checkLoadAndKmCost(docketObj , shiftObj , rateCard , costParameterObj , graceObj):
    try:
        date_= docketObj.shiftDate
        driverDocketLoadSize = docketObj.cubicMl 
        

        driverDocketKm = 0 if float(docketObj.noOfKm) <= float(graceObj.load_km_grace) else float(docketObj.noOfKm) - float(graceObj.load_km_grace)
        # return  driverDocketKm
        driverLoadKmCostTotal = (float(driverDocketLoadSize) * float(costParameterObj.loading_cost_per_cubic_meter)) + (float(driverDocketKm) * float(costParameterObj.km_cost) * float(driverDocketLoadSize))
        
        if shiftObj.shiftType == 'Day':
            shiftType = ThresholdDayShift.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
        else:
            shiftType = ThresholdNightShift.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
            
        if  float(driverDocketLoadSize) < float(shiftType.min_load_in_cubic_meters) :
            docketObj.minimumLoad = (float(shiftType.min_load_in_cubic_meters) - float(driverDocketLoadSize))*float(costParameterObj.loading_cost_per_cubic_meter)
            docketObj.minimumLoad = docketObj.minimumLoad +  (float(driverDocketKm) * float(costParameterObj.km_cost) * float(driverDocketLoadSize))
            docketObj.save()
            
        
        return round(driverLoadKmCostTotal,2)
 
 
    except Exception as e :
        return -404

def checkMinLoadCost(docketObj , shiftObj , rateCard , costParameterObj , graceObj):
    try:
        
        driverDocketLoadSize = docketObj.cubicMl 
        date_= docketObj.shiftDate
        driverDocketKm = 0 if float(docketObj.noOfKm) <= float(graceObj.load_km_grace) else float(docketObj.noOfKm) - float(graceObj.load_km_grace)
        if shiftObj.shiftType == 'Day':
            shiftType = ThresholdDayShift.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
        else:
            shiftType = ThresholdNightShift.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
        # minLoad Cost 
        if  float(driverDocketLoadSize) < float(shiftType.min_load_in_cubic_meters) :
            docketObj.minimumLoad = (float(shiftType.min_load_in_cubic_meters) - float(driverDocketLoadSize))* float(costParameterObj.loading_cost_per_cubic_meter)
            docketObj.minimumLoad = float(docketObj.minimumLoad) +  (float(driverDocketKm) * float(costParameterObj.km_cost) * (float(shiftType.min_load_in_cubic_meters) - float(driverDocketLoadSize)))
            docketObj.save()
            
            return round(docketObj.minimumLoad,2)
        return 0
        
    except Exception as e : 
        
        return -404.0 

def checkSurcharge(docketObj , shiftObj , rateCard , costParameterObj , graceObj):
    
    
    return 0
    # try:
        
    #     # date_= datetime.strptime(docketDate, "%Y-%m-%d").date()
    #     date_= docketDate

    #     driverDocketObj = DriverDocket.objects.filter(docketNumber=driverDocketNumber,shiftDate=date_).first()
        
    #     if 'nosurcharge' in driverDocketObj.surcharge_type.surcharge_Name.lower():
    #         return 0
        
    #     if 'fixed' in  driverDocketObj.surcharge_type.surcharge_Name.lower():
    #         tripObj = DriverTrip.objects.filter(pk = driverDocketObj.tripId.id).first()
    #         adminTruckObj = AdminTruck.objects.filter(adminTruckNumber = tripObj.truckNo).first()
    #         clientTruckConnectionObj = ClientTruckConnection.objects.filter(truckNumber = adminTruckObj,startDate__lte = date_,endDate__gte = date_, clientId = tripObj.clientName).first()
            
    #         rateCard = clientTruckConnectionObj.rate_card_name
    #         costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
          
    #         surchargeAmount = round(costParameterObj.surcharge_cost,2)
    #         if surchargeAmount is None:
    #             return 0
    #         else :
    #             return surchargeAmount
    #     else:
    #         return 0
            

    # except Exception as e :
    #     return -404.0
        
def checkWaitingTime(docketObj , shiftObj , rateCard , costParameterObj , graceObj):
    try:
        date_= docketObj.shiftDate
        docketObj.totalWaitingInMinute = timeDifference(docketObj.waitingTimeStart,docketObj.waitingTimeEnd)
        
        totalWaitingTime = float(docketObj.totalWaitingInMinute) + float(graceObj.waiting_time_grace_in_minutes )
        if float(totalWaitingTime) > float(graceObj.chargeable_waiting_time_starts_after):
            totalWaitingTime = float(totalWaitingTime) - float(graceObj.waiting_time_grace_in_minutes)
            if totalWaitingTime > 0: 
                totalWaitingCost = float(totalWaitingTime) * float(costParameterObj.waiting_cost_per_minute)        
            else:
                totalWaitingCost = 0
            return round(totalWaitingCost,2) 
        else:
            return 0
        
    except Exception as e :
        return -404.0
    

def checkStandByTotal( docketObj , shiftObj , rateCard , costParameterObj , graceObj, slotSize):
    try:
        if slotSize > 0:
            date_= docketObj.shiftDate
            finalStandByCost = 0
            if docketObj.standByStartTime.strip() == '' and docketObj.standByEndTime.strip() == '':
                return 0
            elif docketObj.standByStartTime.strip() != '' and docketObj.standByEndTime.strip() != '':
                finalStandByCost = slotSize * costParameterObj.standby_cost_per_slot
        else:
            finalStandByCost = 0     
        return round(finalStandByCost,2)  

    except Exception as e :
        return -404.0
      
def checkTransferCost(docketObj , shiftObj , rateCard , costParameterObj , graceObj):
    try:
        
        # date_= datetime.strptime(docketDate, "%Y-%m-%d").date()
        date_= docketObj.shiftDate
        driverDocketTransferKm = 0 if float(docketObj.transferKM) <= float(graceObj.transfer_km_grace) else float(docketObj.transferKM) - float(graceObj.transfer_km_grace)
        driverDocketTransferKmCostTotal = float(driverDocketTransferKm) * float(costParameterObj.transfer_cost)
        
        return round(driverDocketTransferKmCostTotal,2)
    except Exception as e : 
        return -404.0

def checkReturnCost(docketObj , shiftObj , rateCard , costParameterObj , graceObj):
    try:
        driverReturnCostTotal = (float(docketObj.returnKm) -  float(graceObj.return_km_grace)) * float(docketObj.returnQty) 
        return round(driverReturnCostTotal,2)
    except Exception as e : 
        return -404.0
    
def checkTotalCost(driverDocketNumber,docketDate ,costDict = costDict):
    try:
        missingComponents = []
        # date_= datetime.strptime(docketDate, "%Y-%m-%d").date()
        date_= docketDate

        driverDocketObj = DriverDocket.objects.filter(docketNumber=driverDocketNumber,shiftDate=date_).first()
        tripObj = DriverTrip.objects.filter(pk = driverDocketObj.tripId.id).first()
        adminTruckObj = AdminTruck.objects.filter(adminTruckNumber = tripObj.truckNo).first()
        clientTruckConnectionObj = ClientTruckConnection.objects.filter(truckNumber = adminTruckObj,startDate__lte = date_,endDate__gte = date_, clientId = tripObj.clientName).first()
        
        rateCard = clientTruckConnectionObj.rate_card_name
        costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
        graceObj = Grace.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
        
        rctiObj = RCTI.objects.filter(docketNumber = driverDocketNumber ,docketDate = date_).first()
        
        driverLoadAndKmCostTotal = costDict['driverDocketCosts']['loadAndKmCost']
        driverWaitingCostTotal = costDict['driverDocketCosts']['waitingTimeCost']
        driverStandByTimeCostTotal = costDict['driverDocketCosts']['standByTotalCost']
        
        costDict = {
            'rctiCosts': {
                'loadAndKmCost':0,
                'surchargeCost':0,
                'waitingTimeCost':0,
                'standByTotalCost':0        
            },
            'driverDocketCosts':{
                'loadAndKmCost':0,
                'surchargeCost':0,
                'waitingTimeCost':0,
                'standByTotalCost':0
            }
        }
        # load 
        # driverLoadAndKmCostTotal =   driverDocketObj.cubicMl * costParameterObj.loading_cost_per_cubic_meter 
        
        # no.ofKm 
        # driverDocketKm = 0 if driverDocketObj.noOfKm <= graceObj.load_km_grace else driverDocketObj.noOfKm - graceObj.load_km_grace
        # driverDocketKmCostTotal = driverDocketKm * costParameterObj.loading_cost_per_cubic_meter * costParameterObj.km_cost
        
        # Transfer Km 
        driverDocketTransferKm = 0 if driverDocketObj.transferKM <= graceObj.transfer_km_grace else driverDocketObj.transferKM - graceObj.transfer_km_grace
        driverDocketTransferKmCostTotal = driverDocketTransferKm * costParameterObj.transfer_cost
        
        
        # return Cost 
        driverReturnCostTotal = (driverDocketObj.returnKm -  graceObj.return_km_grace) * driverDocketObj.returnQty 
        
        # waiting Time 
        # driverWaitingCostTotal =  0
        # if driverDocketObj.totalWaitingInMinute > graceObj.chargeable_waiting_time_starts_after:
        #     totalWaitingTime = driverDocketObj.totalWaitingInMinute - graceObj.waiting_time_grace_in_minutes
        #     driverWaitingCostTotal = totalWaitingTime * costParameterObj.waiting_cost_per_minute
        
        # standby Time
        # start = datetime.strptime(driverDocketObj.standByStartTime,'%H:%M:%S')
        # end = datetime.strptime(driverDocketObj.standByEndTime,'%H:%M:%S')
        # DriverStandByTime = ((end-start).total_seconds())/60
        # driverStandByTimeCostTotal = 0
        # if DriverStandByTime > graceObj.chargeable_standby_time_starts_after:
        #     totalStandByTime = DriverStandByTime - graceObj.standby_time_grace_in_minutes
        #     standBySlot = totalStandByTime/costParameterObj.standby_time_slot_size
        #     if standBySlot >=1:
        #         driverStandByTimeCostTotal = (standBySlot//1) * costParameterObj.standby_cost_per_slot

        # otherCost 
        driverOtherCostTotal = driverDocketObj.others
        
        finalDriverCost = driverLoadAndKmCostTotal  + driverDocketTransferKmCostTotal + driverReturnCostTotal + driverWaitingCostTotal + driverStandByTimeCostTotal + driverOtherCostTotal
                           
        rctiTotalCost = rctiObj.cartageTotalExGST + rctiObj.transferKMTotalExGST + rctiObj.returnKmTotalExGST + rctiObj.waitingTimeSCHEDTotalExGST + rctiObj.waitingTimeTotalExGST + rctiObj.standByTotalExGST + rctiObj.minimumLoadTotalExGST + rctiObj.surchargeTotalExGST + rctiObj.othersTotalExGST

        # Missing parameters
        if (driverLoadAndKmCostTotal > 0 and rctiObj.cartageTotalExGST == 0) or (driverLoadAndKmCostTotal == 0 and rctiObj.cartageTotalExGST > 0) :
            missingComponents.append('Load Km Cost')
            
        if (driverDocketTransferKmCostTotal > 0 and rctiObj.transferKMTotalExGST == 0) or (driverDocketTransferKmCostTotal == 0 and rctiObj.transferKMTotalExGST > 0) :
            missingComponents.append('Transfer Cost')
            
        if (driverReturnCostTotal > 0 and rctiObj.returnKmTotalExGST == 0) or (driverReturnCostTotal == 0 and rctiObj.returnKmTotalExGST > 0):
            missingComponents.append('Return Cost')
            
        if (driverStandByTimeCostTotal > 0  and rctiObj.standByTotalExGST == 0) or (driverStandByTimeCostTotal == 0  and rctiObj.standByTotalExGST > 0):
            missingComponents.append('Waiting Cost')
            
        if (driverWaitingCostTotal > 0 and rctiObj.waitingTimeTotalExGST == 0) or (driverWaitingCostTotal == 0 and rctiObj.waitingTimeTotalExGST > 0):
            missingComponents.append('Standby Cost')

        if (driverOtherCostTotal > 0 and rctiObj.minimumLoadTotalExGST == 0) or (driverOtherCostTotal == 0 and rctiObj.minimumLoadTotalExGST > 0):
            missingComponents.append('Minimum Load Cost')
            
        if finalDriverCost == rctiTotalCost:
            return [round(finalDriverCost,2),round(rctiTotalCost,2), True , missingComponents]
        else:
            return [round(finalDriverCost,2),round(rctiTotalCost,2), False , missingComponents]
            
    except Exception as e :

        return ['','Missing Components not calculated']
    
def checkMissingComponents(reconciliationReportObj):

    components = ''
    if reconciliationReportObj.driverLoadAndKmCost > 0 and reconciliationReportObj.rctiLoadAndKmCost == 0:
        components += 'Load Km Cost' + ', '
    if reconciliationReportObj.driverSurchargeCost > 0 and reconciliationReportObj.rctiSurchargeCost == 0:
        components += 'Surcharge Cost' + ', '
    if reconciliationReportObj.driverWaitingTimeCost > 0 and reconciliationReportObj.rctiWaitingTimeCost == 0:
        components += 'Waiting Time Cost' + ', '
    if reconciliationReportObj.driverTransferKmCost > 0 and reconciliationReportObj.rctiTransferKmCost == 0:
        components += 'Transfer Km Cost' + ', '
    if reconciliationReportObj.driverReturnKmCost > 0 and reconciliationReportObj.rctiReturnKmCost == 0:
        components += 'Return Km Cost' + ', '
    if reconciliationReportObj.driverStandByCost > 0 and reconciliationReportObj.rctiStandByCost == 0:
        components += 'Stand By Cost' + ', '
    if reconciliationReportObj.driverLoadDeficit > 0 and reconciliationReportObj.rctiLoadDeficit == 0:
        components += 'Load Deficit Cost' + ', '
    if reconciliationReportObj.driverBlowBack > 0 and reconciliationReportObj.rctiBlowBack == 0:
        components += 'Blow Back Cost' + ', '
    if reconciliationReportObj.driverCallOut > 0 and reconciliationReportObj.rctiCallOut == 0:
        components += 'Call Out Cost' + ', '
    reconciliationReportObj.missingComponent = components
    reconciliationReportObj.save()

    
    

def DriverTripCheckStandByTotal(docketObj , shiftObj , rateCard , costParameterObj , graceObj):

    tripObj = DriverShiftTrip.objects.filter(pk=docketObj.tripId).first()
    try:
        if tripObj:
            totalStandByTime = getTimeDifference(docketObj.standByStartTime,docketObj.standByEndTime)
            standBySlot = 0
            if float(totalStandByTime) > float(graceObj.chargeable_standby_time_starts_after):
                totalStandByTime = float(totalStandByTime) - float(graceObj.standby_time_grace_in_minutes)
                standBySlot = totalStandByTime//costParameterObj.standby_time_slot_size
            return standBySlot
    except:
        return -404
