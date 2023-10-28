from Account_app.models import *
from GearBox_app.models import *
from django.utils import timezone 
import datetime
from django.shortcuts import get_object_or_404


def checkLoadAndKmCost(rctiTotalExGst,driverDocketNumber,docketDate):
    try:
        date_= datetime.datetime.strptime(docketDate, "%Y-%m-%d").date()
        # print(date_)
        # print(rctiTotalExGst ,driverDocketNumber ,docketDate)
        driverDocketObj = DriverDocket.objects.filter(docketNumber=driverDocketNumber).first()
        # driverDocketKm = driverDocketObj.noOfKm * 2
        driverDocketLoadSize = driverDocketObj.cubicMl 

        tripObj = DriverTrip.objects.filter(pk = driverDocketObj.tripId.id).first()
        clientTruck = ClientTruckConnection.objects.filter(clientTruckId = tripObj.truckNo).first()
        rateCard = clientTruck.rate_card_name
        costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard.id,start_date__lt = date_).first()
        
        graceObj = Grace.objects.filter(rate_card_name = rateCard.id,start_date__lt = date_).first()
        
        if driverDocketObj.noOfKm <= 3:                 
            driverDocketKm = 0
        else:
            # change 3 to km gress
            
            driverDocketKm = driverDocketObj.noOfKm - graceObj.load_km_grace
        driverLoadKmCostTotal = (driverDocketLoadSize * costParameterObj.loading_cost_per_cubic_meter) + (driverDocketKm * costParameterObj.km_cost * driverDocketLoadSize)
    
        if  round(rctiTotalExGst,2) == round(driverLoadKmCostTotal,2):
            # return True
            return (rctiTotalExGst,driverLoadKmCostTotal) 

        else:
            return (rctiTotalExGst,driverLoadKmCostTotal) 
    except Exception as e :
        print(f'Load And Km Cost : {e}')
        return False

def checkSurcharge(rctiSurchargeExGst,driverDocketNumber,docketDate):
    try:
        
        date_= datetime.datetime.strptime(docketDate, "%Y-%m-%d").date()
        driverDocketObj = DriverDocket.objects.filter(docketNumber=driverDocketNumber).first()
        
        if 'nosurcharge' in driverDocketObj.surcharge_type.surcharge_Name.lower():
            return True
        
        if 'fixed' in  driverDocketObj.surcharge_type.surcharge_Name.lower():
            tripObj = DriverTrip.objects.filter(pk = driverDocketObj.tripId.id).first()
            clientTruck = ClientTruckConnection.objects.filter(clientTruckId = tripObj.truckNo).first()
            rateCard = clientTruck.rate_card_name
            costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard.id,start_date__lt = date_).first()
            if costParameterObj.surcharge_cost == rctiSurchargeExGst:
                return True
            else:
                return False
            

    except Exception as e :
        print(f'Surcharge : {e}')
        return False
    
    
def checkWaitingTime(rctiWaitingTimeInMinute,driverDocketNumber,docketDate):
    try:
        date_= datetime.datetime.strptime(docketDate, "%Y-%m-%d").date()
        driverDocketObj = DriverDocket.objects.filter(docketNumber=driverDocketNumber).first()
        tripObj = DriverTrip.objects.filter(pk = driverDocketObj.tripId.id).first()
        clientTruck = ClientTruckConnection.objects.filter(clientTruckId = tripObj.truckNo).first()
        rateCard = clientTruck.rate_card_name
        costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard.id,start_date__lt = date_).first()
        graceObj = Grace.objects.filter(rate_card_name = rateCard.id,start_date__lt = date_).first()
        
        if driverDocketObj.totalWaitingInMinute == rctiWaitingTimeInMinute:
            return True
        else:
            return False

    except Exception as e :
        print(f'Waiting Time : {e}')
        return False
    
    