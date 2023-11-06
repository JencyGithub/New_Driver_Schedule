from Account_app.models import *
from GearBox_app.models import *
from datetime import datetime, timedelta
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User , Group


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
    'RCTI' : RCTI,

    'PublicHoliday':PublicHoliday,
    'User' : User ,
    'Surcharge' : Surcharge
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

def docketFileSave(docketFile,docketNumber = None,returnVal ='default'):
    time = (str(timezone.now())).replace(':', '').replace('-', '').replace(' ', '').split('.')
    time = time[0]
    pdf_folder_path = 'static/img/docketFiles'
    fileName = docketFile.name
    docket_new_filename = time + '!_@' +  str(docketNumber) + '.' + fileName.split('.')[-1]
    pfs = FileSystemStorage(location=pdf_folder_path)
    pfs.save(docket_new_filename, docketFile)
    if returnVal != 'default':
        return docket_new_filename
    else:
        return 'static/img/docketFiles/' + docket_new_filename

def loadFileSave(loadFile):
    time = (str(timezone.now())).replace(':', '').replace('-', '').replace(' ', '').split('.')
    time = time[0]
    pdf_folder_path = 'static/img/finalloadSheet'
    loadFileName = loadFile.name
    load_new_filename = 'Load_Sheet' + time +  '!_@' + loadFileName.replace(" ", "").replace("\t", "")   ##time + '!_@' +  '.' + fileName.split('.')[-1]
    pfs = FileSystemStorage(location=pdf_folder_path)
    pfs.save(load_new_filename, loadFile)
    return 'static/img/finalloadSheet/' + load_new_filename


def getYesterdayDate(curDate):
    try:
        date_obj = datetime.strptime(curDate, "%Y-%m-%d")
        yesterday = date_obj - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        return yesterday_str
    except ValueError:
        return None

    
def getTimeDifference(startDate,endDate):
    try:
        # print(startDate,endDate)
        startDate = int(startDate[0:2])*60 + int(startDate[3:5])
        endDate = int(endDate[0:2])*60 + int(endDate[3:5])
        print(startDate,endDate)
        return abs(endDate-startDate)
    except Exception as e:
        return e


def getMaxTimeFromTwoTime(time1, time2, type=None):
    time1_str = time1.split(':')
    time2_str = time2.split(':')
    
    if type == None:
        if int(time1_str[0] )> int(time2_str[0]):
            return time1
        elif int(time1_str[0]) == int(time2_str[0]):
            if int(time1_str[1]) > int(time2_str[1]):
                return time1
            else:
                return time2
        else:
            return time2
    else:
        if int(time1_str[0]) < int(time2_str[0]):
            return time1
        elif int(time1_str[0]) == int(time2_str[0]):
            if int(time1_str[1]) < int(time2_str[1]):
                return time1
            else:
                return time2
        else:
            return time2
        
    

