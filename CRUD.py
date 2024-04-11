from Account_app.models import *
from GearBox_app.models import *
from Appointment_app.models import *
from datetime import datetime, timedelta
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User , Group
import pytz

def getDatabase(request):
    return request.session.db_name

def dateConverterFromTableToPageFormate(date):
    formated_data = str(date).split()[0]
    return formated_data

def timeDifference(startTime,endTime):
    try:
        startTime = startTime.strftime('%H:%M:%S')
    except:
        pass
    try:
        endTime = endTime.strftime('%H:%M:%S')
    except:
        pass
    start_datetime = datetime.strptime(startTime, '%H:%M:%S')
    end_datetime = datetime.strptime(endTime, '%H:%M:%S')
    time_difference_minutes = (end_datetime - start_datetime).total_seconds() / 60
    return  time_difference_minutes

    
    # if len(time[0]) <= 1:
    #     data = '0'+time[0]+'-'+time[1]+''+time[2]
    #     return data
    
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
    'PreStart' : PreStart,
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

def truckFileSave(truckFile):
    time = (str(timezone.now())).replace(':', '').replace('-', '').replace(' ', '').split('.')
    time = time[0]
    file_path = 'static/TruckFiles'
    truckFileName = truckFile.name
    new_filename = 'truck Files' + time +  '!_@' + truckFileName.replace(" ", "").replace("\t", "")   ##time + '!_@' +  '.' + fileName.split('.')[-1]
    pfs = FileSystemStorage(location=file_path)
    pfs.save(new_filename, truckFile)
    return 'static/TruckFiles/' + new_filename


def getYesterdayDate(curDate):
    try:
        date_obj = datetime.strptime(curDate, "%Y-%m-%d")
        yesterday = date_obj - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        return yesterday_str
    except ValueError:
        return None

    
def getTimeDifference(startTime,endTime):
    try:
        if startTime != 'None' and endTime != 'None':
            startTime = int(startTime[0:2])*60 + int(startTime[3:5])
            endTime = int(endTime[0:2])*60 + int(endTime[3:5])
            return abs(endTime-startTime)
        else:
            return 0
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
  
def getCurrentTimeInString():
    time = (str(timezone.now())).replace(':', '').replace('-', '').replace(' ', '').split('.')
    return time[0]
    

def holcimDateConvertStr(str_):
    val_ = str_.split('T',)
    val_ = val_[0]+ ' '+val_[1]
    return val_


def getCurrentDateTimeObj():
    # currentTimezone = pytz.timezone('Asia/Kolkata')
    # currentDateTime = datetime.now(tz=currentTimezone)
    # return currentDateTime
    return datetime.now()

def formatDateTimeForDBSave(dateTimeStr):
    if dateTimeStr:
        dateTimeStr = datetime.strptime(dateTimeStr, "%Y-%m-%dT%H:%M")  
    else:
        dateTimeStr = None
    return dateTimeStr

def dateTimeObj(dateStr=None, time=None, dateTimeObj=None, dateTimeStr=None):
    if dateTimeStr:
        dateStr, time = map(str, dateTimeStr.split())
        year, month, day = map(int, dateStr.split('-'))
        hours, minutes, seconds = map(int, time.split(':'))
        return datetime(int(year), int(month), int(day), int(hours), int(minutes), int(seconds))
    if dateTimeObj:
        return datetime.fromisoformat(dateTimeObj)
    elif dateStr and time:
        year, month, day = map(int, dateStr.split('-'))
        hours, minutes, seconds = map(int, time.split(':'))
        return datetime(int(year), int(month), int(day), int(hours), int(minutes), int(seconds))
    elif dateStr:
        year, month, day = map(int, dateStr.split('-')) 
        return date(int(year), int(month), int(day))
    elif time:
        hours, minutes, seconds = map(int, time.split(':'))
        return time(int(hours), int(minutes), int(seconds))
    else:
        return None

# driverShift form admin side 

def dateTimeConvertIntoDate(data):
    formatted_string = data.strftime("%Y-%m-%d %H:%M:%S.%f%z")
    datetime_object = datetime.fromisoformat(formatted_string)
    date_only = datetime_object.date()
    return date_only


from django.db.models import Q

def checkTruckAndDriverAvailability(shiftObj, tripObj, endDateTime, startDateTime):
    driverId = shiftObj.driverId
    truckConnectionId = tripObj.truckConnectionId

    existing_trips = DriverShiftTrip.objects.filter(
        ~Q(shiftId=shiftObj.id), 
        Q(truckConnectionId = truckConnectionId) , 
        Q( Q(startDateTime__lte=endDateTime, endDateTime__gte=endDateTime) | Q( startDateTime__lte=startDateTime, endDateTime__gte=startDateTime ,)| Q( startDateTime__gte = startDateTime , endDateTime__lte = endDateTime ,) |Q(startDateTime__lte=startDateTime, endDateTime__gte=endDateTime))
    )
    
    existing_shifts = DriverShift.objects.filter(
        ~Q(pk=shiftObj.id), 
        Q(driverId = driverId) , 
        Q( Q(startDateTime__lte=endDateTime, endDateTime__gte=endDateTime) | Q( startDateTime__lte=startDateTime, endDateTime__gte=startDateTime ,)| Q( startDateTime__gte = startDateTime , endDateTime__lte = endDateTime ,) |Q(startDateTime__lte=startDateTime, endDateTime__gte=endDateTime))
    )
    print(existing_shifts,existing_trips)
    if existing_shifts or existing_trips:
        return False
    else:
        return True
        
