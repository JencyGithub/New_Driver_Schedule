from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
import pandas as pd
from Account_app.reconciliationUtils import  *
from datetime import time
import sys

def run():
    with open(r"scripts/addSurchargeToRateCard.txt", 'r') as f:
        surchargeName = f.read().strip().lower()
        # print(f'Surcharge Name: {surchargeName}')
        
    newSurchargeObj = Surcharge()
    newSurchargeObj.surcharge_Name = surchargeName
    newSurchargeObj.save()

    # data = data.split(',')[0:-1]
    rateCards = RateCard.objects.all()

    for ratecard in rateCards:
        costParameterQuerySet = CostParameters.objects.filter(rate_card_name=ratecard)
        
        for costParameterObj in costParameterQuerySet:
            ratecardVariantStartDate = costParameterObj.start_date
            ratecardVariantEndDate = costParameterObj.end_date
            
            # print(costParameterObj.id, ratecardVariantStartDate, ratecardVariantEndDate)
            
            newSurchargeValueObj = RateCardSurchargeValue()
            newSurchargeValueObj.rate_card_name = ratecard
            newSurchargeValueObj.surchargeValue = 0
            newSurchargeValueObj.start_date = ratecardVariantStartDate
            newSurchargeValueObj.end_date = ratecardVariantEndDate
            newSurchargeValueObj.surcharge = newSurchargeObj
            newSurchargeValueObj.save()