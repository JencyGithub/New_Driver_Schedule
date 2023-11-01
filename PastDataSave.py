import pandas as pd
from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
from Account_app.reconciliationUtils import  *

def insertIntoDatabase(data,key,fileName):
    existingTrip = None
    
    # Trip save
    try:
        existingTrip = DriverTrip.objects.filter(truckNo = data[1],shiftDate = data[0]).values().first()
        
        if existingTrip:
            tripObj = DriverTrip.objects.get(pk=existingTrip['id'])
        else:
            driverName = data[4].strip().replace(' ','').lower()
            client = Client.objects.get_or_create(name = 'Boral')[0]
            driver = Driver.objects.get(name = driverName)
            shiftType = 'Day'
            shiftDate =  str(data[0]).split(' ')[0]
            
            tripObj = DriverTrip(
                verified = True,
                driverId = driver,
                clientName = client,
                shiftType = shiftType,
                truckNo = data[1],
                shiftDate = shiftDate
            )
            tripObj.save()

        # Docket save
        existingDockets = DriverDocket.objects.filter(tripId = tripObj.id).count()
        tripObj.numberOfLoads = existingDockets + 1
                
        if tripObj.startTime and tripObj.endTime:
            tripObj.startTime = getMaxTimeFromTwoTime(str(tripObj.startTime),str(data[6]),'min')
            tripObj.endTime = getMaxTimeFromTwoTime(str(tripObj.endTime),str(data[7]))
        else:
            tripObj.startTime = str(data[6])
            tripObj.endTime = str(data[7])
            
        tripObj.save()

        basePlant = BasePlant.objects.get_or_create(basePlant = "Not selected")[0] 
        surCharge = Surcharge.objects.get_or_create(surcharge_Name = 'Nosurcharge')[0]
            
        docketObj = DriverDocket()

        docketObj.shiftDate = ' ' if str(data[0]) == 'nan' else data[0]
        docketObj.tripId = tripObj
        docketObj.docketNumber = data[5]
        docketObj.noOfKm = 0 if str(data[10]) == 'nan' else data[10]
        docketObj.transferKM = 0 if str(data[18]) == 'nan' else data[18]
        docketObj.returnToYard = True if data[16] == 'Yes' else False
        docketObj.returnQty = 0 if str(data[14]) == 'nan' else data[14]
        docketObj.returnKm = 0 if str(data[15]) == 'nan' else data[15]
        docketObj.waitingTimeStart = 0 if str(data[11]) == 'nan' else data[11]
        docketObj.waitingTimeEnd = 0 if str(data[12]) == 'nan' else data[12]
        docketObj.totalWaitingInMinute = 0 if str(data[13]) == 'nan' else data[13]
        docketObj.cubicMl = 0 if str(data[8]) == 'nan' else data[8]
        docketObj.standByStartTime = ' ' if str(data[20]) == 'nan' else data[20]
        docketObj.standByEndTime = ' ' if str(data[21]) == 'nan' else data[21]
        docketObj.comment = data[17]
        docketObj.basePlant = basePlant
        docketObj.surcharge_type = surCharge
        # surcharge_duration = 
        # others = 
        docketObj.save()
            
        reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = docketObj.docketNumber , docketDate = docketObj.shiftDate ).first()
        # print(reconciliationDocketObj)
                
        if not  reconciliationDocketObj :
            reconciliationDocketObj = ReconciliationReport()
        
        driverLoadAndKmCost = checkLoadAndKmCost(int(docketObj.docketNumber),docketObj.shiftDate)
        driverSurchargeCost = checkSurcharge(int(docketObj.docketNumber),docketObj.shiftDate)
        driverWaitingTimeCost = checkWaitingTime(int(docketObj.docketNumber),docketObj.shiftDate)
        driverStandByCost = checkStandByTotal(int(docketObj.docketNumber),docketObj.shiftDate)
        driverTransferKmCost = checkTransferCost(int(docketObj.docketNumber),docketObj.shiftDate)
        driverReturnKmCost = checkReturnCost(int(docketObj.docketNumber),docketObj.shiftDate)
             
        # minLoad 
        driverLoadDeficit = checkMinLoadCost(docketObj.docketNumber,docketObj.shiftDate)
        # TotalCost 
        driverTotalCost = driverLoadAndKmCost +driverSurchargeCost + driverWaitingTimeCost + driverStandByCost + driverTransferKmCost + driverReturnKmCost +driverLoadDeficit

        reconciliationDocketObj.docketNumber = int(docketObj.docketNumber) 
        reconciliationDocketObj.docketDate = docketObj.shiftDate  
        reconciliationDocketObj.driverLoadAndKmCost = driverLoadAndKmCost 
        reconciliationDocketObj.driverSurchargeCost = driverSurchargeCost 
        reconciliationDocketObj.driverWaitingTimeCost = driverWaitingTimeCost 
        reconciliationDocketObj.driverStandByCost = driverStandByCost 
        reconciliationDocketObj.driverLoadDeficit = driverLoadDeficit 
        reconciliationDocketObj.driverTransferKmCost = driverTransferKmCost 
        reconciliationDocketObj.driverReturnKmCost = driverReturnKmCost  
        reconciliationDocketObj.driverTotalCost = driverTotalCost 
        reconciliationDocketObj.save()
        # missingComponents 
        checkMissingComponents(reconciliationDocketObj)
        
    except Exception as e:
        # print(f"Error : {e}, Row: {key}")    
        # print(f"Error : {data}")          
        pastTripErrorObj = PastTripError(
            tripDate = data[0].strftime('%Y-%m-%d'),
            docketNumber = data[5],
            lineNumber = key,
            errorFromPastTrip = e,
            fileName = fileName.split('@_!')[-1]
        )
        pastTripErrorObj.save()
        
    return True

f = open("pastTrip_entry.txt", 'r')
file_name = f.read()

fileName = f'static/Account/PastTripsEntry/{file_name}'

txtFile = open('static/subprocessFiles/errorFromPastTrip.txt','w')
txtFile.write(f'File:{file_name}\n\n')
txtFile.close()

pastData = pd.read_excel(fileName)


for key,row in pastData.iterrows():
    try:
        insertIntoDatabase(row,key,fileName)
    except Exception as e:
        print(f" ! Error : {e}")


        