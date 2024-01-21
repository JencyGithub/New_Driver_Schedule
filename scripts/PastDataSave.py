# import pandas as pd
from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
from Account_app.reconciliationUtils import  *
from datetime import time
import warnings

def run():
    warnings.filterwarnings('ignore')
    f = open(r"pastTrip_entry.txt", 'r')
    file_name = f.read()
    
    monthFileName = open(r"pastTrip_entry_month.txt",'r')
    monthAndYear = monthFileName.read()

    fileName = f'static/Account/PastTripsEntry/{file_name}'
    # fileName = f'static/Account/PastTripsEntry/20231202141345@_!20231202112629@_!April1-152023.csv'

    txtFile = open(r'static/subprocessFiles/errorFromPastTrip.txt','w')
    txtFile.write(f'File:{file_name}\n\n')
    txtFile.close()

    with open(fileName, 'r') as pastData:
        count = 0
        for line in pastData:
            try:
                if '"' in line:
                   line = str(line).replace('"','')
                if "'" in line:
                   line =  str(line).replace("'","")
                count += 1
                if count == 1:
                    continue
                data = line.split(',')

                if len(data) != 25:
                    pastTripErrorObj = PastTripError(
                                    clientName = 'boral',
                                    tripDate = res_,
                                    docketNumber = data[5],
                                    truckNo = data[1],
                                    lineNumber = count,
                                    errorFromPastTrip = "File Data in wrong format.",
                                    fileName = fileName.split('@_!')[-1],
                                    data = data
                                )                    
                    pastTripErrorObj.save()
                    continue
                
                        
                
                if ' ' in str(data[0]):
                    res_ = str(data[0]).split()[0]
                elif '/' in str(data[0]):
                    str_ = str(data[0]).split('/')
                    res_ = str_[-1]+'-'+str_[-2]+'-'+str_[0]
                else:
                    res_ = str(data[0])

                # with open(r'pastDataRow.txt','a') as f:
                #     f.write(str(data[0]) + '\n')
                # print(count)
                shiftDate = datetime.strptime(res_, '%Y-%m-%d')
                startTime = datetime.strptime(str(data[6]), '%H:%M:%S').time()
                startTimeDateTime = datetime.combine(shiftDate.date(), startTime)
                startTimeStr = startTimeDateTime.strftime('%Y-%m-%d %H:%M:%S')
                # print(getMaxTimeFromTwoTime(str(startTimeStr),startTimeStr,'min'))
                
                endTime = datetime.strptime(str(data[7]), '%H:%M:%S').time()
                endTimeDateTime = datetime.combine(shiftDate.date(),endTime)
                endTimeStr =endTimeDateTime.strftime('%Y-%m-%d %H:%M:%S')
                # print('shiftDate',data[6],data[7])

                if res_.split('-')[1] != monthAndYear.split('-')[-1] or res_.split('-')[0] != monthAndYear.split('-')[0]:
                    pastTripErrorObj = PastTripError(
                                clientName = 'boral',
                                tripDate = res_,
                                docketNumber = data[5],
                                truckNo = data[1],
                                lineNumber = count,
                                errorFromPastTrip = "Incorrect month/year values present in file.",
                                fileName = fileName.split('@_!')[-1],
                                data = data
                            ) 
                            # print('grace card not found')                   
                    pastTripErrorObj.save()
                    continue
                    

                driverName = data[4].strip().replace(' ','').lower()
                clientObj = Client.objects.filter(name = 'boral').first()
                
                driverObj = Driver.objects.filter(name = driverName).first()
                if driverObj:
                    
                    # Trip save
                    try:
                        basePlant = BasePlant.objects.filter(basePlant = data[24].strip().upper()).first() 
                        if basePlant is None:
                            pastTripErrorObj = PastTripError(
                                    clientName = 'boral',
                                    tripDate = res_,
                                    docketNumber = data[5],
                                    truckNo = data[1],
                                    lineNumber = count,
                                    errorFromPastTrip = "BasePlant does not exist.",
                                    fileName = fileName.split('@_!')[-1],
                                    data = data
                                ) 
                            pastTripErrorObj.save()
                            continue
                        shiftObj = DriverShift.objects.filter(shiftDate = shiftDate , driverId = driverObj.driverId).first()
                        if shiftObj is None:
                            shiftObj = DriverShift()
                            shiftObj.shiftDate =  shiftDate
                            shiftObj.driverId =  driverObj.driverId
                            shiftObj.shiftType = 'Day'
                            shiftObj.verified = True
                            shiftObj.save()
                            
                        shiftId = shiftObj.id
                        
                        clientTruckConnectionObj = ClientTruckConnection.objects.filter(clientTruckId = data[1] , startDate__lte = shiftDate,endDate__gte = shiftDate, clientId = clientObj.clientId).first()
                        if clientTruckConnectionObj is None:
                            pastTripErrorObj = PastTripError(
                                clientName = 'boral',
                                tripDate = res_,
                                docketNumber = data[5],
                                truckNo = data[1],
                                lineNumber = count,
                                errorFromPastTrip = "Client truck connection object does not exist.",
                                fileName = fileName.split('@_!')[-1],
                                data = data
                            )
                            pastTripErrorObj.save()
                            continue
                        
                        tripObj = DriverShiftTrip.objects.filter(shiftId = shiftId , truckConnectionId = clientTruckConnectionObj.id).first()
                        if tripObj is None:
                            print('Creating New Trip')
                            
                            tripObj = DriverShiftTrip()
                            tripObj.verified = True
                            tripObj.shiftId = shiftId
                            tripObj.clientId = clientObj.clientId
                            
                            tripObj.truckConnectionId = clientTruckConnectionObj.id
                            # print('truckConnection ',clientTruckConnectionObj,tripObj)
                            
                            tripObj.save()
                            print('Trip Obj Created')
                        print('tripId',tripObj.id)

                        # Docket save
                        # existingDockets = DriverShiftDocket.objects.filter(tripId = tripObj.id,shiftId = shiftObj.id).count()
                        # tripObj.numberOfLoads = existingDockets + 1
                        
                        
                        # if tripObj.startDateTime and tripObj.endDateTime :
                        #     tripObj.startDateTime = getMaxTimeFromTwoTime(str(tripObj.startDateTime),str(data[6]),'min').strip()
                        #     tripObj.endDateTime = getMaxTimeFromTwoTime(str(tripObj.endDateTime),str(data[7])).strip()
                        #     print('startTime  Set' , tripObj.startDateTime)
                        #     print('EndTime Set' , tripObj.endDateTime)
                            
                        # else:
                        #     tripObj.startDateTime =getMaxTimeFromTwoTime(str(data[6]),str(data[6]),'min').strip()
                        #     tripObj.endDateTime = getMaxTimeFromTwoTime(str(data[7]),str(data[7])).strip()
                        #     print('Else startTime  Set' , tripObj.startDateTime)
                        #     print('Else EndTime Set' , tripObj.endDateTime)
                        shiftDate = datetime.strptime(res_, '%Y-%m-%d')
                        startTime = datetime.strptime(str(data[6]).strip(), '%H:%M:%S').time()
                        startTimeDateTime = datetime.combine(shiftDate.date(), startTime)
                        endTime = datetime.strptime(str(data[7]).strip(), '%H:%M:%S').time()
                        endTimeDateTime = datetime.combine(shiftDate.date(),endTime)  
                        if tripObj.startDateTime and tripObj.endTime :
                            print('Start Date time Inside if')
                            if tripObj.startDateTime > startTimeDateTime:
                                tripObj.startDateTime = startTimeDateTime
                            if tripObj.endDateTime < endTimeDateTime:
                                tripObj.endDateTime = endTimeDateTime
                            print('startDateTime  Set' , tripObj.startDateTime)
                            print('EndDateTime Set' , tripObj.endDateTime)
                        else:
                            print('Start Date time Inside Else')
                            
                            
                            tripObj.startDateTime =startTimeDateTime
                            tripObj.endDateTime = endTimeDateTime
                            print('Else startTime  Set' , tripObj.startDateTime)
                            print('Else EndTime Set' , tripObj.endDateTime)
                        shiftObj.startDateTime = tripObj.startDateTime
                        if count == 5:
                            exit() 
                        # print('shift' , shiftObj.startDateTime)
                                         
                        shiftObj.endDateTime = tripObj.endDateTime
                        shiftObj.save()
                        tripObj.save()

                        surCharge = Surcharge.objects.filter(surcharge_Name = 'No Surcharge').first()
                        docketObj = DriverShiftDocket.objects.filter(docketNumber = data[5] , tripId=tripObj.id).first()
                        if docketObj :
                            pastTripErrorObj = PastTripError(
                                    clientName = 'boral',
                                    tripDate = res_,
                                    docketNumber = data[5],
                                    truckNo = data[1],
                                    lineNumber = count,
                                    errorFromPastTrip = "DocketNumber already Exist for this trip.",
                                    fileName = fileName.split('@_!')[-1],
                                    data = data
                                ) 
                            pastTripErrorObj.save()
                            continue
                        docketObj = DriverShiftDocket()                


                        clientTruckConnectionObj = ClientTruckConnection.objects.filter(clientTruckId = data[1] , startDate__lte = shiftDate,endDate__gte = shiftDate, clientId = clientObj.clientId).first()

                        if clientTruckConnectionObj:
                            # print("finding ratecard")
                            rateCard = clientTruckConnectionObj.rate_card_name                        
                            graceObj = Grace.objects.filter(rate_card_name = rateCard,start_date__lte = tripObj.shiftDate,end_date__gte = tripObj.shiftDate).first()
                            if not graceObj:
                                pastTripErrorObj = PastTripError(
                                    clientName = 'boral',
                                    tripDate = res_,
                                    docketNumber = data[5],
                                    truckNo = data[1],
                                    lineNumber = count,
                                    errorFromPastTrip = "No matching grace card for the date.",
                                    fileName = fileName.split('@_!')[-1],
                                    data = data
                                ) 
                                # print('grace card not found')                   
                                pastTripErrorObj.save()
                                continue

                            costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard).first()

                            if not costParameterObj:
                                pastTripErrorObj = PastTripError(
                                    clientName = 'boral',
                                    tripDate = res_,
                                    docketNumber = data[5],
                                    truckNo = data[1],
                                    lineNumber = count,
                                    errorFromPastTrip = "No matching cost parameter card for the date.",
                                    fileName = fileName.split('@_!')[-1],
                                    data = data
                                )                    
                                pastTripErrorObj.save()
                                # print('COST PARAMETER not found')
                                continue
                                

                                
                            docketObj.shiftDate = shiftDate
                            docketObj.tripId = tripObj.id
                            docketObj.docketNumber = data[5]
                            docketObj.noOfKm = 0 if str(data[10]).lower() == '' else data[10]
                            docketObj.transferKM = 0 if str(data[18]).lower() == '' else data[18]
                            docketObj.returnToYard = True if data[16].lower() == 'yes' else False
                            docketObj.returnQty = 0 if str(data[14]).lower() == '' else data[14]
                            docketObj.returnKm = 0 if str(data[15]).lower() == '' else data[15]
                            docketObj.waitingTimeStart = '00:00:00' if str(data[11]).strip().lower() == '' else str(datetime.strptime(data[11], '%H:%M:%S').time()) 
                            docketObj.waitingTimeEnd = '00:00:00' if str(data[12]).strip().lower() == '' else str(datetime.strptime(data[12], '%H:%M:%S').time())
                            # docketObj.totalWaitingInMinute = totalWaitingTime
                            docketObj.cubicMl = 0 if str(data[8]).lower() == '' else data[8]
                            docketObj.standByStartTime ='00:00:00' if str(data[20]).lower() == '' else str(datetime.strptime(data[20], '%H:%M:%S').time())
                            docketObj.standByEndTime ='00:00:00' if str(data[21]).lower() == '' else str(datetime.strptime(data[21], '%H:%M:%S').time())
                            # docketObj.standBySlot = standBySlot
                            docketObj.comment = data[17]
                            # modification for adding blow back and replacement.
                            if data[19].strip().replace(' ','') != None:
                                docketObj.comment = docketObj.comment + 'Blow back comment : ' + data[19].strip() 
                                
                            if data[23].strip().replace(' ','') != None:
                                docketObj.comment = docketObj.comment + 'Replacement comment : ' + data[23].strip() 
                                
                            
                            docketObj.basePlant = basePlant.id
                            docketObj.surcharge_type = surCharge.id
                            # surcharge_duration = 
                            # others = 
                            docketObj.save()
                            reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = docketObj.docketNumber, docketDate=docketObj.shiftDate , clientId = clientObj.clientId).first()
                        
                            if not  reconciliationDocketObj :
                                reconciliationDocketObj = ReconciliationReport()
                                
                                
                            reconciliationDocketObj.driverId = driverObj.driverId  
                            reconciliationDocketObj.clientId = clientObj.clientId
                            reconciliationDocketObj.truckId = tripObj.truckConnectionId
                            
                            # for ReconciliationReport 
                            clientTruckConnectionObj = ClientTruckConnection.objects.filter(pk=tripObj.truckConnectionId,startDate__lte = docketObj.shiftDate,endDate__gte = docketObj.shiftDate, clientId = clientObj).first()
                            rateCard = clientTruckConnectionObj.rate_card_name
                            costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard.id,start_date__lte = docketObj.shiftDate,end_date__gte = docketObj.shiftDate).first()
                            graceObj = Grace.objects.filter(rate_card_name = rateCard.id,start_date__lte = docketObj.shiftDate,end_date__gte = docketObj.shiftDate).first()
                            
                            driverLoadAndKmCost = checkLoadAndKmCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                            
                            driverSurchargeCost = checkSurcharge(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)

                            driverWaitingTimeCost = checkWaitingTime(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                            slotSize = DriverTripCheckStandByTotal(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                            driverStandByCost = checkStandByTotal(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj,slotSize =slotSize)
                            driverTransferKmCost = checkTransferCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                            driverReturnKmCost = checkReturnCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                            # minLoad 
                            driverLoadDeficit = checkMinLoadCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                            # TotalCost 
                            driverTotalCost = driverLoadAndKmCost +driverSurchargeCost + driverWaitingTimeCost + driverStandByCost + driverTransferKmCost + driverReturnKmCost +driverLoadDeficit
                            reconciliationDocketObj.docketNumber = docketObj.docketNumber  
                            reconciliationDocketObj.docketDate = shiftObj.shiftDate 
                            reconciliationDocketObj.driverLoadAndKmCost = driverLoadAndKmCost 
                            reconciliationDocketObj.driverSurchargeCost = driverSurchargeCost 
                            reconciliationDocketObj.driverWaitingTimeCost = driverWaitingTimeCost 
                            reconciliationDocketObj.driverStandByCost = driverStandByCost 
                            reconciliationDocketObj.driverLoadDeficit = driverLoadDeficit 
                            reconciliationDocketObj.driverTransferKmCost = driverTransferKmCost 
                            reconciliationDocketObj.driverReturnKmCost = driverReturnKmCost  
                            reconciliationDocketObj.driverTotalCost = round(driverTotalCost,2)
                            reconciliationDocketObj.fromDriver = True 
                            reconciliationDocketObj.save()
                            # print("reconciliation done!!!!")
                        
                        else:
                            pastTripErrorObj = PastTripError(
                                clientName = 'boral',
                                tripDate = res_,
                                docketNumber = data[5],
                                truckNo = data[1],
                                lineNumber = count,
                                errorFromPastTrip = "Client truck connection object does not exist.",
                                fileName = fileName.split('@_!')[-1],
                                data = data
                            )
                            pastTripErrorObj.save()
                    except Exception as e:       
                        pastTripErrorObj = PastTripError(
                            clientName = 'boral',
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = count,
                            errorFromPastTrip = e,
                            fileName = fileName.split('@_!')[-1],
                            data = data
                        )
                        pastTripErrorObj.save()
                else:
                    pastTripErrorObj = PastTripError(
                            clientName = 'boral',
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = count,
                            errorFromPastTrip = 'Driver matching query does not exist.',
                            fileName = fileName.split('@_!')[-1],
                            data = data
                        )
                    pastTripErrorObj.save()
                    
                    
            except Exception as e:
                pastTripErrorObj = PastTripError(
                        clientName = 'boral',
                        tripDate = res_,
                        docketNumber = data[5],
                        truckNo = data[1],
                        lineNumber = count,
                        errorFromPastTrip = e,
                        fileName = fileName.split('@_!')[-1],
                        data = data
                    )
                pastTripErrorObj.save()
                
