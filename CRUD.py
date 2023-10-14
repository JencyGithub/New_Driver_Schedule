from Account_app.models import *
from GearBox_app.models import *

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
        
