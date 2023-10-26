from Account_app.models import *
from GearBox_app.models import *
from django.utils import timezone 
import datetime
from django.shortcuts import get_object_or_404


def checkLoadAndKmCost(rctiTotalExGst,driverDocketNumber,docketDate):
    try:
        date_= datetime.datetime.strptime(docketDate, "%Y-%m-%d").date()
        # print(date_)
        print(rctiTotalExGst ,driverDocketNumber ,docketDate)
        driverDocketObj = DriverDocket.objects.filter(docketNumber=driverDocketNumber).first()
        driverDocketKm = driverDocketObj.noOfKm * 2
        driverDocketLoadSize = driverDocketObj.cubicMl 
        
        
        tripObj = DriverTrip.objects.filter(pk = driverDocketObj.tripId.id).first()
        
        clientTruck = ClientTruckConnection.objects.filter(clientTruckId = tripObj.truckNo).first()
    
    
        rateCard = clientTruck.rate_card_name

        costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard,start_date__lt = date_).first()
        
        # driverLoadKmCostUnitPrice = costParameterObj.loading_cost_per_cubic_meter + costParameterObj.km_cost
        
        driverLoadKmCostTotal = (driverDocketLoadSize * costParameterObj.loading_cost_per_cubic_meter) + (driverDocketKm  * costParameterObj.km_cost)
        print(rctiTotalExGst , driverLoadKmCostTotal)
    
        if  rctiTotalExGst == round(driverLoadKmCostTotal,2):
            return True
        else:
            return False 
    except Exception as e :
        print(f'exception : {e}')
        return False

