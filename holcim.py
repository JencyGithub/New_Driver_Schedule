import pandas as pd
from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
from Account_app.reconciliationUtils import  *
from datetime import time
import re 
def dateConvert(dataList,type_):
    try:
        if dataList.lower() != 'nan':
            timestamp_obj = datetime.strptime(dataList, '%d/%m/%Y %I:%M:%S %p')
            if type_ =='date':
                date_only_str = timestamp_obj.strftime('%Y-%m-%d')
                return date_only_str
            elif type_ == 'time':
                time_only_str = timestamp_obj.strftime('%H:%M:%S')
                return time_only_str
        else:
            date_only_str = None  
        return date_only_str
    except Exception as e:
        return None
    

def dateTimeConvert(dataList):
    try:
        if pd.isna(dataList) or str(dataList).lower() == 'nan':
            return None
        else:
            try:
                timestamp_obj = datetime.strptime(str(dataList),  '%Y-%m-%d %H:%M:%S')
            except: 
                timestamp_obj = datetime.strptime(str(dataList), '%d/%m/%Y %I:%M:%S %p')
            formatted_timestamp = timestamp_obj.strftime('%Y-%m-%d %H:%M:%S')
            return formatted_timestamp
    except ValueError as e:
        return None
    
    
def insertIntoHolcimModel(key,dataList , file_name):
    if len(dataList) == 44 :
        try:
            driverId = Driver.objects.filter(name = dataList[40].strip().replace(' ','').lower()).first()
            if driverId is None:
                rctiErrorObj = RctiErrors( 
                            clientName = 'holcim',
                            docketNumber = str(dataList[4]),
                            docketDate = dateTimeConvert(dataList[8]),
                            errorDescription = 'Driver matching query does not exist.',
                            fileName = file_name,
                            data = str(dataList)
                )
                rctiErrorObj.save()
                return 
                
            vehicleNumber = '[0-9]{4,4}'
            
            try:
                re.fullmatch(vehicleNumber , dataList[0])
                try:
                    existingTrip = HolcimTrip.objects.filter(truckNo = int(dataList[0]) , shiftDate = dateConvert(dataList[8],'date')).values().first()
                    if existingTrip:
                        holcimTripObj = HolcimTrip.objects.get(pk=existingTrip['id'])
                    else:
                        holcimTripObj = HolcimTrip(
                            truckNo = int(dataList[0]),
                            shiftDate = dateConvert(str(dataList[8]),'date')
                        )
                        holcimTripObj.save()
                    existingDockets = HolcimDocket.objects.filter(tripId = holcimTripObj.id).count()
                    try:
                        currentMatchingDocket = HolcimDocket.objects.filter(tripId =  holcimTripObj.id,jobNo = dataList[4], truckNo = int(dataList[0]) ,ticketedDate = dateConvert(dataList[8],'date')).first()
                        if currentMatchingDocket:
                            rctiErrorObj = RctiErrors( 
                                clientName = 'holcim',
                                docketNumber = str(dataList[4]),
                                docketDate = dateTimeConvert(dataList[8]),
                                errorDescription = 'Docket already exist.',
                                fileName = file_name,
                                data = str(dataList)
                            )
                            rctiErrorObj.save()
                            return
                    except Exception as e:
                        pass
                    
                    holcimTripObj.numberOfLoads = existingDockets + 1
                    holcimTripObj.save()  
                    holcimDocketObj = HolcimDocket()
                    holcimDocketObj.truckNo  = int(dataList[0])
                    holcimDocketObj.tripId  = holcimTripObj
                    holcimDocketObj.jobNo  =  dataList[4]
                    if holcimDocketObj.jobNo == 'nan':
                        rctiErrorObj = RctiErrors( 
                                clientName = 'holcim',
                                docketNumber = holcimDocketObj.jobNo,
                                docketDate = dateTimeConvert(dataList[8]),
                                errorDescription = 'Job No. Miss match',
                                fileName = file_name,
                                data = str(dataList)
                            )
                        rctiErrorObj.save()
                        return 
                    holcimDocketObj.orderNo  = 0 if str(dataList[2]) == 'nan' else dataList[2]
                    holcimDocketObj.status  = 0 if str(dataList[6]) == 'nan' else dataList[6]
                    holcimDocketObj.ticketedDate  =  dateConvert(dataList[8],'date')
                    holcimDocketObj.ticketedTime  =  dateConvert(dataList[8],'time')
                    if holcimDocketObj.ticketedDate is None:
                        rctiErrorObj = RctiErrors( 
                            clientName = 'holcim',
                            docketNumber = holcimDocketObj.jobNo,
                            docketDate = dateTimeConvert(dataList[8]),
                            errorDescription = 'Ticketed Miss match',
                            fileName = file_name,
                            data = str(dataList)
                        )
                        rctiErrorObj.save()
                        return 
                    holcimDocketObj.load  =  dateTimeConvert(dataList[13])
                    holcimDocketObj.loadComplete  = 0 if str(dataList[15]) == 'nan' else dataList[15]
                    holcimDocketObj.toJob  =  dateTimeConvert(dataList[16])
                    
                    holcimDocketObj.timeToDepart  = 0 if str(dataList[18]) == 'nan' else dataList[18]
                    holcimDocketObj.onJob  =  dateTimeConvert(dataList[19])
                    holcimDocketObj.timeToSite  = 0 if str(dataList[21]) == 'nan' else dataList[21]
                    holcimDocketObj.beginUnload  = dateTimeConvert(dataList[22])
                    holcimDocketObj.waitingTime  = 0 if str(dataList[24]) == 'nan' else dataList[24]
                    holcimDocketObj.endPour  = dateTimeConvert(dataList[25])
                    holcimDocketObj.wash  =dateTimeConvert(dataList[26])
                    holcimDocketObj.toPlant  =  dateTimeConvert(dataList[27])
                    holcimDocketObj.timeOnSite  = 0 if str(dataList[32]) == 'nan' else dataList[32]
                    holcimDocketObj.atPlant  =  dateTimeConvert(dataList[33])
                    holcimDocketObj.leadDistance  = 0 if str(dataList[35]) == 'nan' else dataList[35]
                    holcimDocketObj.returnDistance  = 0 if str(dataList[36]) == 'nan' else dataList[36]
                    holcimDocketObj.totalDistance  = 0 if str(dataList[37]) == 'nan' else dataList[37]
                    holcimDocketObj.totalTime  = 0 if str(dataList[38]) == 'nan' else dataList[38]
                    holcimDocketObj.waitTimeBetweenJob  = 0 if str(dataList[39]) == 'nan' else dataList[39]
                    holcimDocketObj.driverName  = driverId #dataList[40]
                    holcimDocketObj.quantity  = 0 if str(dataList[41]) == 'nan' else dataList[41]
                    holcimDocketObj.slump  = 0 if str(dataList[42]) == 'nan' else dataList[42]
                    holcimDocketObj.waterAdded  = 0 if str(dataList[43]) == 'nan' else str(dataList[43]).replace('(','').replace('L','').replace(')','').strip()
                    holcimDocketObj.save()
                except Exception as e:
                    rctiErrorObj = RctiErrors( 
                            clientName = 'holcim',
                            docketNumber = holcimDocketObj.jobNo,
                            docketDate = dateTimeConvert(dataList[8]),
                            errorDescription = e,
                            fileName = file_name,
                            data = str(dataList)
                        )
                    rctiErrorObj.save()
                    pass
            except:
                pass
        except Exception as e:
            pass
    else:
        pass
   

with open(r"File_name_file.txt", 'r') as f:
    file_name = f.read()


file = f'static/Account/RCTI/RCTIInvoice/{file_name}'


# file = 'static/Account/RCTI/RCTIInvoice/20231210053127@_!holcim.xlsx'
data = pd.read_excel(file)
try:
    for key,row in data.iterrows():
        try:
            int(row[0])
            insertIntoHolcimModel(key,row,file_name)
        except:
            pass
except Exception as e:
    pass
        
