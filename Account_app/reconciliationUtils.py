from Account_app.models import *
from GearBox_app.models import *
from django.utils import timezone 
import datetime
from django.shortcuts import get_object_or_404
from CRUD import *
# from datetime import strptime

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
def checkLoadAndKmCost(rctiTotalExGst,driverDocketNumber,docketDate,costDict=costDict):
    try:
        date_= datetime.strptime(docketDate, "%Y-%m-%d").date()
        driverDocketObj = DriverDocket.objects.filter(docketNumber=driverDocketNumber,shiftDate=date_).first()
        driverDocketLoadSize = driverDocketObj.cubicMl 

        tripObj = DriverTrip.objects.filter(pk = driverDocketObj.tripId.id).first()
        adminTruckObj = AdminTruck.objects.filter(adminTruckNumber = tripObj.truckNo).first()
        clientTruckConnectionObj = ClientTruckConnection.objects.filter(truckNumber = adminTruckObj,startDate__lte = date_,endDate__gte = date_, clientId = tripObj.clientName).first()
        
        rateCard = clientTruckConnectionObj.rate_card_name
        costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
        
        graceObj = Grace.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
        driverDocketKm = 0 if driverDocketObj.noOfKm <= graceObj.load_km_grace else driverDocketObj.noOfKm - graceObj.load_km_grace
        driverLoadKmCostTotal = (driverDocketLoadSize * costParameterObj.loading_cost_per_cubic_meter) + (driverDocketKm * costParameterObj.km_cost * driverDocketLoadSize)

        if tripObj.shiftType == 'Day':
            shiftType = ThresholdDayShift.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
        else:
            shiftType = ThresholdNightShift.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
            
        if  driverDocketLoadSize < shiftType.min_load_in_cubic_meters :
            driverDocketObj.others = (shiftType.min_load_in_cubic_meters - driverDocketLoadSize)*costParameterObj.loading_cost_per_cubic_meter
            driverDocketObj.others = driverDocketObj.others +  (driverDocketKm * costParameterObj.km_cost * driverDocketLoadSize)
            driverDocketObj.save()
            
        costDict['rctiCosts']['loadAndKmCost'] = round(rctiTotalExGst,2)
        costDict['driverDocketCosts']['loadAndKmCost'] = round(driverLoadKmCostTotal,2)
        if  round(rctiTotalExGst,2) == round(driverLoadKmCostTotal,2):
            return [round(rctiTotalExGst,2) , round(driverLoadKmCostTotal,2),True] 

        else:
            return [round(rctiTotalExGst,2) , round(driverLoadKmCostTotal,2),False] 
 
    except Exception as e :
        # print(f'{driverDocketNumber}Load And Km Cost : {e}')
        return ['','',False]

def checkSurcharge(rctiSurchargeExGst,driverDocketNumber,docketDate, costDict = costDict):
    try:
        
        date_= datetime.strptime(docketDate, "%Y-%m-%d").date()
        driverDocketObj = DriverDocket.objects.filter(docketNumber=driverDocketNumber,shiftDate=date_).first()
        
        if 'nosurcharge' in driverDocketObj.surcharge_type.surcharge_Name.lower():
            costDict['rctiCosts']['surchargeCost'] = round(rctiSurchargeExGst,2)
            costDict['driverDocketCosts']['surchargeCost'] = 0
            return ['No surcharge','',True]
        
        if 'fixed' in  driverDocketObj.surcharge_type.surcharge_Name.lower():
            tripObj = DriverTrip.objects.filter(pk = driverDocketObj.tripId.id).first()
            adminTruckObj = AdminTruck.objects.filter(adminTruckNumber = tripObj.truckNo).first()
            clientTruckConnectionObj = ClientTruckConnection.objects.filter(truckNumber = adminTruckObj,startDate__lte = date_,endDate__gte = date_, clientId = tripObj.clientName).first()
            
            rateCard = clientTruckConnectionObj.rate_card_name
            costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
          
            costDict['rctiCosts']['surchargeCost'] = round(rctiSurchargeExGst,2)
            costDict['driverDocketCosts']['surchargeCost'] = round(costParameterObj.surcharge_cost,2)
            
            if round(costParameterObj.surcharge_cost,2) == round(rctiSurchargeExGst,2):
                return [round(rctiSurchargeExGst,2), round(costParameterObj.surcharge_cost,2) ,True ]
            else:
                return [round(rctiSurchargeExGst,2) ,round(costParameterObj.surcharge_cost,2),False ]

            

    except Exception as e :
        # print(f'{driverDocketNumber}Surcharge : {e}')
        return ['','',False]
        
def checkWaitingTime(rctiWaitingTimeTotalExGST,driverDocketNumber,docketDate , costDict= costDict):
    try:
        date_= datetime.strptime(docketDate, "%Y-%m-%d").date()
        driverDocketObj = DriverDocket.objects.filter(docketNumber=driverDocketNumber,shiftDate=date_).first()
        tripObj = DriverTrip.objects.filter(pk = driverDocketObj.tripId.id).first()
        adminTruckObj = AdminTruck.objects.filter(adminTruckNumber = tripObj.truckNo).first()
        clientTruckConnectionObj = ClientTruckConnection.objects.filter(truckNumber = adminTruckObj,startDate__lte = date_,endDate__gte = date_, clientId = tripObj.clientName).first()
        
        rateCard = clientTruckConnectionObj.rate_card_name
        costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
        graceObj = Grace.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
        
        if driverDocketObj.totalWaitingInMinute > graceObj.chargeable_waiting_time_starts_after:
            totalWaitingTime = driverDocketObj.totalWaitingInMinute - graceObj.waiting_time_grace_in_minutes
            if totalWaitingTime > 0: 
                totalWaitingCost = totalWaitingTime * costParameterObj.waiting_cost_per_minute        
            else:
                totalWaitingCost = 0
                
            costDict['rctiCosts']['waitingTimeCost'] = round(rctiWaitingTimeTotalExGST,2)
            costDict['driverDocketCosts']['waitingTimeCost'] = round(totalWaitingCost,2)
            
            if round(totalWaitingCost,2) == round(rctiWaitingTimeTotalExGST,2):
                return [ round(rctiWaitingTimeTotalExGST,2), round(totalWaitingCost,2) ,True]
            else:
                
                return [round(rctiWaitingTimeTotalExGST,2), round(totalWaitingCost,2) , False]

        else:
            return True
        
    except Exception as e :
        # print(f'{driverDocketNumber}Waiting Time : {e}')
        return ['','',False]
    
def checkStandByTotal(rctiStandByTotalExGST,driverDocketNumber,docketDate, costDict = costDict):
    try:
        
        date_= datetime.strptime(docketDate, "%Y-%m-%d").date()
        driverDocketObj = DriverDocket.objects.filter(docketNumber=driverDocketNumber,shiftDate=date_).first()
        finalStandByCost = 0
        
        if rctiStandByTotalExGST == 0 and driverDocketObj.standByStartTime.strip() == '' and driverDocketObj.standByEndTime.strip() == '':
            return [f'No stand by component.','', True]
        
        elif driverDocketObj.standByStartTime.strip() != '' and driverDocketObj.standByEndTime.strip() != '':
            tripObj = DriverTrip.objects.filter(pk = driverDocketObj.tripId.id).first()
            adminTruckObj = AdminTruck.objects.filter(adminTruckNumber = tripObj.truckNo).first()
            clientTruckConnectionObj = ClientTruckConnection.objects.filter(truckNumber = adminTruckObj,startDate__lte = date_,endDate__gte = date_, clientId = tripObj.clientName).first()
            
            rateCard = clientTruckConnectionObj.rate_card_name
            costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
            graceObj = Grace.objects.filter(rate_card_name = rateCard.id,start_date__lte = date_,end_date__gte = date_).first()
            
            start = datetime.strptime(driverDocketObj.standByStartTime,'%H:%M:%S')
            end = datetime.strptime(driverDocketObj.standByEndTime,'%H:%M:%S')
            DriverStandByTime = ((end-start).total_seconds())/60
            
            if DriverStandByTime > graceObj.chargeable_standby_time_starts_after:
                totalStandByTime = DriverStandByTime - graceObj.standby_time_grace_in_minutes
                standBySlot = totalStandByTime/costParameterObj.standby_time_slot_size
                
                if standBySlot >=1:
                    finalStandByCost = (standBySlot//1) * costParameterObj.standby_cost_per_slot
                # elif standBySlot > 0:
                #     finalStandByCost = 0.5 * costParameterObj.standby_cost_per_slot
                
            else:
                return [finalStandByCost,rctiStandByTotalExGST,False]   
            
        costDict['rctiCosts']['standByTotalCost'] = round(rctiStandByTotalExGST,2)
        costDict['driverDocketCosts']['standByTotalCost'] = round(finalStandByCost,2)
        
        if round(finalStandByCost,2) == round(rctiStandByTotalExGST,2):
            return [round(rctiStandByTotalExGST,2), round(finalStandByCost,2), True]
        else:
            return [round(rctiStandByTotalExGST,2), round(finalStandByCost,2),False] 
        
    except Exception as e :
        # print(f'{driverDocketNumber}Standby time : {e}')
        return ['','',False]
      
def checkTotalCost(driverDocketNumber,docketDate ,costDict = costDict):
    try:
        missingComponents = []
        date_= datetime.strptime(docketDate, "%Y-%m-%d").date()
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
                           
        rctiTotalCost = rctiObj.cartageTotal + rctiObj.transferKMTotal + rctiObj.returnKmTotal + rctiObj.waitingTimeSCHEDTotal + rctiObj.waitingTimeTotal + rctiObj.standByTotal + rctiObj.minimumLoadTotal + rctiObj.surchargeTotal + rctiObj.othersTotal

        # Missing parameters
        if (driverLoadAndKmCostTotal > 0 and rctiObj.cartageTotal == 0) or (driverLoadAndKmCostTotal == 0 and rctiObj.cartageTotal > 0) :
            missingComponents.append('Load Km Cost')
            
        if (driverDocketTransferKmCostTotal > 0 and rctiObj.transferKMTotal == 0) or (driverDocketTransferKmCostTotal == 0 and rctiObj.transferKMTotal > 0) :
            missingComponents.append('Transfer Cost')
            
        if (driverReturnCostTotal > 0 and rctiObj.returnKmTotal == 0) or (driverReturnCostTotal == 0 and rctiObj.returnKmTotal > 0):
            missingComponents.append('Return Cost')
            
        if (driverStandByTimeCostTotal > 0  and rctiObj.standByTotal == 0) or (driverStandByTimeCostTotal == 0  and rctiObj.standByTotal > 0):
            missingComponents.append('Waiting Cost')
            
        if (driverWaitingCostTotal > 0 and rctiObj.waitingTimeTotal == 0) or (driverWaitingCostTotal == 0 and rctiObj.waitingTimeTotal > 0):
            missingComponents.append('Standby Cost')

        if (driverOtherCostTotal > 0 and rctiObj.minimumLoadTotal == 0) or (driverOtherCostTotal == 0 and rctiObj.minimumLoadTotal > 0):
            missingComponents.append('Minimum Load Cost')
            
        if finalDriverCost == rctiTotalCost:
            return [round(finalDriverCost,2),round(rctiTotalCost,2), True , missingComponents]
        else:
            return [round(finalDriverCost,2),round(rctiTotalCost,2), False , missingComponents]
            
    except Exception as e :
        # print(f'{driverDocketNumber}Total cost : {e}')
        # return ['',False,'Missing Components not calculated']
        return ['','Missing Components not calculated']