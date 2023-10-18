from Account_app.models import *
from GearBox_app.models import *
from datetime import datetime


def dateConverterFromTableToPageFormate(date):
    formated_data = str(date).split()[0]
    return formated_data

model_mapping = {
    'Client' : Client,
    'AdminTruck' : AdminTruck,
    'Driver' : Driver,
    'ClientTruckConnection' : ClientTruckConnection,
    'NatureOfLeave' : NatureOfLeave,
    'LeaveRequest' : LeaveRequest,
    'BasePlant' : BasePlant,
    'DriverTrip' : DriverTrip,
    'DriverDocket' : DriverDocket,
    'PastTrip' : PastTrip,
    'RCTI' : RCTI,
    'RCTIDocketAdjustment' : RCTIDocketAdjustment
}

def insertIntoTable(tableName:str,dataSet:dict,model_mapping=model_mapping):
    try :
        if tableName in model_mapping:
            model = model_mapping.get(tableName)
            model.objects.create(**dataSet)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return f"{e}"
    
def updateIntoTable(record_id,tableName:str,dataSet:dict,model_mapping=model_mapping):
    try :
        if tableName in model_mapping:
            model = model_mapping.get(tableName)            
            record = model.objects.get(pk=record_id)
            for key, value in dataSet.items():
                setattr(record, key, value)
            record.save()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return f"{e}"

# Date convert : 2018-02-28 to date(year,month,day)    
def dateConvert(givenDate):
    givenDate = givenDate.split('-')
    formattedDate = date(int(givenDate[0]),int(givenDate[1]),int(givenDate[2]))
    return formattedDate
