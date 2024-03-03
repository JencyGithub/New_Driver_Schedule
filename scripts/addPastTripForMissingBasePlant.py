from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
from Account_app.reconciliationUtils import  *
from datetime import time
import csv , re
from variables import *

f = open(r"scripts/addPastTripForMissingBasePlant.txt", 'r')
basePlantName = f.read()

matchingData = PastTripError.objects.filter(errorFromPastTrip="BasePlant does not exist.", status=False)

# For PastTrip 
for i in matchingData:
    try:
        data = i.data
        data = data.replace('[','').replace(']','').replace('\\n','').replace("'",'')
        data = data.split(',')
        

        if ' ' in str(data[0].strip()):
            res_ = str(data[0].strip()).split()[0]
        elif '/' in str(data[0].strip()):
            str_ = str(data[0].strip()).split('/')
            res_ = str_[-1]+'-'+str_[-2]+'-'+str_[0]
        else:
            res_ = str(data[0].strip())


        shiftDate = datetime.strptime(res_, '%Y-%m-%d')
        pastBasePlant = data[-1].strip().upper()

        startTime = datetime.strptime(str(data[6].strip()), '%H:%M:%S').time()
        startTimeDateTime = datetime.combine(shiftDate.date(), startTime)
        startTimeStr = startTimeDateTime.strftime('%Y-%m-%d %H:%M:%S')
        
        endTime = datetime.strptime(str(data[7].strip()), '%H:%M:%S').time()
        endTimeDateTime = datetime.combine(shiftDate.date(),endTime)
        endTimeStr =endTimeDateTime.strftime('%Y-%m-%d %H:%M:%S')
        clientObj = Client.objects.filter(name = i.clientName).first()
        # driverName = data[4].strip().replace(' ','').lower()
        driverID = int(data[4].strip())
        driverObj = Driver.objects.filter(driverId=driverID).first()
        # driverObj = Driver.objects.filter(name = driverName).first()
        basePlant = BasePlant.objects.filter(basePlant = basePlantName).first()
        if pastBasePlant == basePlant.basePlant:
            i.status = True
            i.save()
            try:
                clientTruckConnectionObj = ClientTruckConnection.objects.filter(clientTruckId = data[1].strip() , startDate__lte = shiftDate,endDate__gte = shiftDate, clientId = clientObj.clientId).first()
                if clientTruckConnectionObj is None:
                    pastTripErrorObj = PastTripError(
                        clientName = i.clientName,
                        tripDate = res_,
                        docketNumber = data[5],
                        truckNo = data[1],
                        lineNumber = i.lineNumber,
                        errorFromPastTrip = "Client truck connection object does not exist.",
                        fileName = i.fileName.split('@_!')[-1],
                        exceptionText ="Client truck connection object does not exist.",
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
                
                
                
                tripObj = DriverShiftTrip.objects.filter(shiftId = shiftId , truckConnectionId = clientTruckConnectionObj.id).first()
                if tripObj is None:
                    # print('Creating New Trip')
                    
                    tripObj = DriverShiftTrip()
                    tripObj.verified = True
                    tripObj.shiftId = shiftId
                    tripObj.clientId = clientObj.clientId
                    
                    tripObj.truckConnectionId = clientTruckConnectionObj.id
                    # print('truckConnection ',clientTruckConnectionObj,tripObj)
                    
                    tripObj.save()
                #     print('Trip Obj Created')
                # print('tripId',tripObj.id)

                # Docket save
                # existingDockets = DriverShiftDocket.objects.filter(tripId = tripObj.id,shiftId = shiftObj.id).count()
                # tripObj.numberOfLoads = existingDockets + 1
                
                shiftDate = datetime.strptime(res_, '%Y-%m-%d')

                try:
                    shiftDateStr = datetime.strftime(shiftDate.date(), '%Y-%m-%d')
                    
                    startTimeDateTime = shiftDateStr + ' ' + data[6].strip()                            
                    endTimeDateTime = shiftDateStr + ' ' + data[7].strip()
                    
                    startTimeDateTime = datetime.strptime(startTimeDateTime, '%Y-%m-%d %H:%M:%S')
                    endTimeDateTime = datetime.strptime(endTimeDateTime, '%Y-%m-%d %H:%M:%S')
                    
                    # print(startTimeDateTime, endTimeDateTime)
                except Exception as e:
                    pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "Incorrect date format",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = e,
                            data = data
                        ) 
                    pastTripErrorObj.save()
                    continue
                
                try:
                    # print(startTimeDateTime.tzinfo, startTimeDateTime)
                    # print(endTimeDateTime.tzinfo, endTimeDateTime)
                    if tripObj.startDateTime and tripObj.endDateTime :
                        # print('Start Date time Inside if')
                        # print(data[5], tripObj.startDateTime.date(),startTimeDateTime.date() , tripObj.startDateTime.time() , startTimeDateTime.time())
                        if tripObj.startDateTime.date() == startTimeDateTime.date() and tripObj.startDateTime.time() > startTimeDateTime.time():
                            tripObj.startDateTime = startTimeDateTime
                            # print('Updating Start Time trip match')
                        if tripObj.endDateTime.date() == endTimeDateTime.date() and tripObj.endDateTime.time() < endTimeDateTime.time():
                            tripObj.endDateTime = endTimeDateTime
                            # print('Updating End Time trip match')
                            
                    else:
                        # print('Start Date time Inside Else')
                        tripObj.startDateTime =startTimeDateTime
                        tripObj.endDateTime = endTimeDateTime
                        # print('Saved Start Time : ', startTimeDateTime ,  'Saved End Time' ,endTimeDateTime )
                except Exception as e:
                    pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "Incorrect date format",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = e,
                            data = data
                        ) 
                    pastTripErrorObj.save()
                    with open('IncorrectDate.txt','a') as f:
                        f.write(f'{e}\n')
                    continue
                
                shiftObj.startDateTime = tripObj.startDateTime
                
                # print('shift' , shiftObj.startDateTime)
                                    
                shiftObj.endDateTime = tripObj.endDateTime
                shiftObj.save()
                tripObj.save()

                surCharge = Surcharge.objects.filter(surcharge_Name = noSurcharge).first()
                docketObj = DriverShiftDocket.objects.filter(docketNumber = data[5].strip() , tripId=tripObj.id , truckConnectionId = tripObj.truckConnectionId).first()
                if docketObj :
                    pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "DocketNumber already Exist for this trip.",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = "DocketNumber already Exist for this trip.",
                            data = data
                        ) 
                    pastTripErrorObj.save()
                    continue
                docketObj = DriverShiftDocket()                
                # print('Docket Obj Created.')

                clientTruckConnectionObj = ClientTruckConnection.objects.filter(clientTruckId = data[1].strip() , startDate__lte = shiftDate,endDate__gte = shiftDate, clientId = clientObj.clientId).first()

                if clientTruckConnectionObj:
                    # print("finding ratecard")
                    rateCard = clientTruckConnectionObj.rate_card_name 
                    graceObj = Grace.objects.filter(rate_card_name = rateCard,start_date__lte = shiftObj.shiftDate,end_date__gte = shiftObj.shiftDate).first()

                    if not graceObj:
                        pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "No matching grace card for the date.",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = "No matching grace card for the date.",
                            data = data
                        ) 
                        # print('grace card not found')                   
                        pastTripErrorObj.save()
                        continue

                    costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard).first()

                    if not costParameterObj:
                        pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "No matching cost parameter card for the date.",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = "No matching cost parameter card for the date.",
                            data = data
                        )                    
                        pastTripErrorObj.save()
                        # print('COST PARAMETER not found')
                        continue
                        

                    try:
                        docketObj.shiftDate = shiftDate
                        docketObj.shiftId = shiftObj.id
                        docketObj.tripId = tripObj.id
                        docketObj.clientId = tripObj.clientId
                        docketObj.truckConnectionId = tripObj.truckConnectionId
                        docketObj.docketNumber = str(data[5].strip())
                        docketObj.noOfKm = 0 if str(data[10].strip()).lower() == '' else data[10].strip()
                        docketObj.transferKM = 0 if str(data[18].strip()).lower() == '' else data[18].strip()
                        docketObj.returnToYard = True if data[16].strip().lower() == 'yes' else False
                        docketObj.returnQty = 0 if str(data[14].strip()).lower() == '' else data[14].strip()
                        docketObj.returnKm = 0 if str(data[15].strip()).lower() == '' else data[15].strip()
                        docketObj.cubicMl = 0 if str(data[8].strip()).lower() == '' else data[8].strip()
                        waitingTimeStart = None if str(data[11]).strip().lower() == '' else str(data[11]).strip().lower()
                        waitingTimeEnd = None if str(data[12]).strip().lower() == '' else str(data[12]).strip().lower()

                        waitingTimeStartCount = 0 
                        waitingTimeEndCount = 0
                        if waitingTimeStart != None:
                            waitingTimeStartCount = waitingTimeStart.count(':')
                        if waitingTimeEnd != None:
                            waitingTimeEndCount = waitingTimeEnd.count(':')

                        if waitingTimeStart is not None and waitingTimeStartCount == 1:
                            waitingTimeStart = str(datetime.strptime(data[11].strip(), '%H:%M').time())
                        elif waitingTimeStartCount == 2:
                            waitingTimeStart = str(datetime.strptime(data[11].strip(), '%H:%M:%S').time())
                        if waitingTimeEnd is not None and waitingTimeEndCount == 1:
                            waitingTimeEnd = str(datetime.strptime(data[12].strip(), '%H:%M').time())
                        elif waitingTimeEndCount == 2:
                            waitingTimeEnd = str(datetime.strptime(data[12].strip(), '%H:%M:%S').time())
                        docketObj.waitingTimeStart = waitingTimeStart
                        docketObj.waitingTimeEnd = waitingTimeEnd
                        # docketObj.totalWaitingInMinute = totalWaitingTime
                        standByStartTime = None if str(data[20]).strip().lower() == '' else str(data[20]).strip().lower()
                        standByEndTime = None if str(data[21]).strip().lower() == '' else str(data[21]).strip().lower()

                        # Initialize counts to 0
                        standByStartCount = 0 
                        standByEndCount = 0
                        if standByStartTime != None:
                            standByStartCount = standByStartTime.count(':')
                        if standByEndTime != None:
                            standByEndCount = standByEndTime.count(':')

                        if standByStartCount == 1 and standByStartTime is not None:
                            standByStartTime = str(datetime.strptime(data[20].strip(), '%H:%M').time())
                        elif standByStartCount == 2:
                            standByStartTime = str(datetime.strptime(data[20].strip(), '%H:%M:%S').time())
                            
                        if standByEndCount == 1 and standByEndTime is not None:
                            standByEndTime = str(datetime.strptime(data[21].strip(), '%H:%M').time())
                        elif standByEndCount == 2:
                            standByEndTime = str(datetime.strptime(data[21].strip(), '%H:%M:%S').time())

                        docketObj.standByStartTime = standByStartTime
                        docketObj.standByEndTime = standByEndTime
                        # docketObj.standBySlot = standBySlot
                        docketObj.comment = data[17].strip()
                        # modification for adding blow back and replacement.
                        if data[19].strip().replace(' ','') != None:
                            docketObj.comment = docketObj.comment + 'Blow back comment : ' + data[19].strip() 
                            
                        if data[23].strip().replace(' ','') != None:
                            docketObj.comment = docketObj.comment + 'Replacement comment : ' + data[23].strip() 
                            
                        
                        docketObj.basePlant = basePlant.id
                        docketObj.surcharge_type = surCharge.id

                        docketObj.save()
                    except Exception as e:
                        pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "Docket Save internal server error.",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = e,
                            data = data
                            )
                        pastTripErrorObj.save()
                        continue
                    try:
                        reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = docketObj.docketNumber, docketDate=docketObj.shiftDate , clientId = clientObj.clientId).first()
                        
                        if not  reconciliationDocketObj :
                            reconciliationDocketObj = ReconciliationReport()
                            
                            
                        reconciliationDocketObj.driverId = driverObj.driverId  
                        reconciliationDocketObj.clientId = clientObj.clientId
                        reconciliationDocketObj.truckConnectionId = tripObj.truckConnectionId
                        
                        # for ReconciliationReport 
                        clientTruckConnectionObj = ClientTruckConnection.objects.filter(pk=tripObj.truckConnectionId,startDate__lte = docketObj.shiftDate,endDate__gte = docketObj.shiftDate, clientId = clientObj).first()
                        rateCard = clientTruckConnectionObj.rate_card_name
                        costParameterObj = CostParameters.objects.filter(rate_card_name = rateCard.id,start_date__lte = docketObj.shiftDate,end_date__gte = docketObj.shiftDate).first()
                        graceObj = Grace.objects.filter(rate_card_name = rateCard.id,start_date__lte = docketObj.shiftDate,end_date__gte = docketObj.shiftDate).first()
                        
                        driverLoadAndKmCost = checkLoadAndKmCost(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                        
                        driverSurchargeCost = checkSurcharge(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                        driverWaitingTimeCost = 0
                        driverStandByCost = 0
                        if docketObj.waitingTimeStart and docketObj.waitingTimeEnd:
                            if graceObj.waiting_load_calculated_on_load_size:
                                driverWaitingTimeCost = checkLoadCalculatedWaitingTime(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                            else:  
                                driverWaitingTimeCost = checkWaitingTime(docketObj=docketObj, shiftObj=shiftObj, rateCard=rateCard, costParameterObj=costParameterObj,graceObj=graceObj)
                            
                        if docketObj.standByStartTime and docketObj.standByEndTime:
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
                    except Exception as e:
                        pastTripErrorObj = PastTripError(
                            clientName = i.clientName,
                            tripDate = res_,
                            docketNumber = data[5],
                            truckNo = data[1],
                            lineNumber = i.lineNumber,
                            errorFromPastTrip = "Reconciliation Entry internal server error.",
                            fileName = i.fileName.split('@_!')[-1],
                            exceptionText = e,
                            data = data
                            )
                        pastTripErrorObj.save()
                        continue
                
                else:
                    pastTripErrorObj = PastTripError(
                        clientName = i.clientName,
                        tripDate = res_,
                        docketNumber = data[5],
                        truckNo = data[1],
                        lineNumber = i.lineNumber,
                        errorFromPastTrip = "Client truck connection object does not exist.",
                        fileName = i.fileName.split('@_!')[-1],
                        data = data
                    )
                    pastTripErrorObj.save()
            except Exception as e:       
                pastTripErrorObj = PastTripError(
                    clientName = i.clientName,
                    tripDate = res_,
                    docketNumber = data[5],
                    truckNo = data[1],
                    lineNumber = i.lineNumber,
                    errorFromPastTrip = e,
                    fileName = i.fileName.split('@_!')[-1],
                    exceptionText = e,
                    data = data
                )
                pastTripErrorObj.save()

    except Exception as e:
        pastTripErrorObj = PastTripError(
            clientName = i.clientName,
            tripDate = res_,
            docketNumber = data[5],
            truckNo = data[1],
            lineNumber = i.lineNumber,
            errorFromPastTrip = e,
            fileName = i.fileName.split('@_!')[-1],
            exceptionText = e,
            data = data
        )
        pastTripErrorObj.save()


# # RCTI FUNCTION 
def convertIntoFloat(str_):
    if '(' in str_:
        str_ = '-'+str_.strip('()')
    cleaned_string = str_.replace(' ','').replace(',','')
    return float(cleaned_string)


# def checkDate(date_):
#     pattern = r'\d{2}/\d{2}/\d{2}'
#     return True if re.fullmatch(pattern,date_) else False

def dateConvert(date_):
    date_ = date_.split('/')
    year_ = '20' + date_[-1]
    return year_ .strip()+ '-' + date_[1].strip() + '-' + date_[0].strip()
    
docket_pattern = r'^\d{8}$|^\d{6}$'
# For RCTI 
rctiMatchingData = RctiErrors.objects.filter(errorDescription="Earning Depot/Location does not exist.", status=False)
# rctiMatchingData = RctiErrors.objects.filter(docketNumber = '26032270' , errorDescription="list index out of range", status=False)
# dataList = "['10652', '20527042', '01/08/23', 'BEGA', '151  AUCKLAND ST BEGA CARTAGE OTHERPER KM PER CU M', '4.0000', '3.0000', 'CUBIC ME', '37.1900', '111.57', '11.16', '122.73']"


for i in rctiMatchingData:
    fileName = i.fileName
    dataList = i.data
    dataList = dataList.replace('[','').replace(']','').replace("'",'')
    dataList = dataList.split(',')
    getReportIdAndLastValue = dataList[-1].split('@_!')
    rctiReportObj = RctiReport.objects.filter(pk=getReportIdAndLastValue[-1]).first()
    dataList[-1] = getReportIdAndLastValue[0]
    clientName = i.clientName
    
    for j in range(len(dataList)):
        dataList[j] = dataList[j].strip()
        # if j ==2:
        #     dataList[2] = dateConvert(dataList[2])
    
    if str(dataList[3]) == basePlantName:
        i.status = True
        i.save()
        try:
            errorSolve = dataList
            RCTIobj = None
            try:
                existingDocket = RCTI.objects.get(docketNumber=int(dataList[1]))
                if str(existingDocket.docketDate) == dateConvert(dataList[2]):
                    RCTIobj = existingDocket
            except:
                RCTIobj = RCTI()
            RCTIobj.truckNo = convertIntoFloat(dataList[0])
            RCTIobj.clientName = Client.objects.filter(name = i.clientName).first()
            if re.match(docket_pattern ,str(dataList[1])):
                RCTIobj.docketNumber = str(dataList[1])
                dataList = dataList[2:]
                while dataList:

                    dump = dataList[:10]
                    
                    description = dump[2].lower().strip()
                    if 'top up' in description:
                        # insertTopUpRecord(dump, RCTIobj.truckNo, RCTIobj.docketNumber)
                        RCTIobj.docketDate = dateConvert(dump[0].split()[-1])
                        RCTIobj.docketYard = dump[1]
                        
                        RCTIobj.others = dump[2]
                        RCTIobj.othersCost = convertIntoFloat(dump[6])
                        RCTIobj.othersGSTPayable = convertIntoFloat(dump[7])
                        RCTIobj.othersTotalExGST = convertIntoFloat(dump[8])
                        RCTIobj.othersTotal = convertIntoFloat(dump[9])
                        dataList = dataList[10:]
                        continue
                        
                    RCTIobj.docketDate = dateConvert(dump[0])
                    RCTIobj.docketYard = dump[1]
                    
                    if "truck transfer" in description:
                        RCTIobj.transferKM = convertIntoFloat(dump[4])
                        RCTIobj.transferKMCost = convertIntoFloat(dump[6])
                        RCTIobj.transferKMGSTPayable = convertIntoFloat(dump[-2])
                        RCTIobj.transferKMTotalExGST = convertIntoFloat(dump[-3])
                        RCTIobj.transferKMTotal = convertIntoFloat(dump[-1])
                    elif "cartage" in description:
                        RCTIobj.noOfKm = convertIntoFloat(dump[3])
                        RCTIobj.cubicMl = convertIntoFloat(dump[4])
                        RCTIobj.cubicMiAndKmsCost = convertIntoFloat(dump[6])
                        RCTIobj.destination = description.split('cartage')[0]
                        RCTIobj.cartageGSTPayable = convertIntoFloat(dump[-2])
                        RCTIobj.cartageTotalExGST = convertIntoFloat(dump[-3])
                        RCTIobj.cartageTotal = convertIntoFloat(dump[-1])
                    elif "return" in description:
                        RCTIobj.returnKm = convertIntoFloat(dump[4])
                        RCTIobj.returnPerKmPerCubicMeterCost = convertIntoFloat(dump[6])
                        RCTIobj.returnKmGSTPayable = convertIntoFloat(dump[-2])
                        RCTIobj.returnKmTotalExGST = convertIntoFloat(dump[-3])
                        RCTIobj.returnKmTotal = convertIntoFloat(dump[-1])
                    elif "waiting time" in description:
                        RCTIobj.waitingTimeInMinutes = convertIntoFloat(dump[4])
                        RCTIobj.waitingTimeCost = convertIntoFloat(dump[6])
                        RCTIobj.waitingTimeGSTPayable = convertIntoFloat(dump[-2])
                        RCTIobj.waitingTimeTotalExGST = convertIntoFloat(dump[-3])
                        RCTIobj.waitingTimeTotal = convertIntoFloat(dump[-1])
                    elif "minimum load" in description:
                        RCTIobj.minimumLoad = convertIntoFloat(dump[4])
                        RCTIobj.loadCost = convertIntoFloat(dump[6])
                        RCTIobj.minimumLoadGSTPayable = convertIntoFloat(dump[-2])
                        RCTIobj.minimumLoadTotalExGST = convertIntoFloat(dump[-3])
                        RCTIobj.minimumLoadTotal = convertIntoFloat(dump[-1])
                    elif "standby" in description:
                        RCTIobj.standByNoSlot = convertIntoFloat(dump[4])
                        RCTIobj.standByUnit = 'slot' if str(
                            dump[5].lower()) == 'each' else 'minute'
                        RCTIobj.standByPerHalfHourDuration = convertIntoFloat(dump[6])
                        RCTIobj.standByGSTPayable = convertIntoFloat(dump[-2])
                        RCTIobj.standByTotalExGST = convertIntoFloat(dump[-3])
                        RCTIobj.standByTotal = convertIntoFloat(dump[-1])
                    elif "surcharge after hours" in description:
                        RCTIobj.surcharge_duration = convertIntoFloat(dump[4])
                        if "mon-fri" in description and "each" in str(dump[5].lower()):
                            RCTIobj.surcharge_fixed_normal = convertIntoFloat(dump[6])
                        elif "sat" in description and 'mon' in description and "each" in str(dump[5].lower()):
                            RCTIobj.surcharge_fixed_sunday = convertIntoFloat(dump[6])
                        RCTIobj.surchargeGSTPayable = convertIntoFloat(dump[-2])
                        RCTIobj.surchargeTotalExGST = convertIntoFloat(dump[-3])
                        RCTIobj.surchargeTotal = convertIntoFloat(dump[-1])
                    elif "waiting time sched" in description:
                        RCTIobj.waitingTimeSCHED = convertIntoFloat(dump[4])
                        RCTIobj.waitingTimeSCHEDCost = convertIntoFloat(dump[6])
                        RCTIobj.waitingTimeSCHEDGSTPayable = convertIntoFloat(dump[-2])
                        RCTIobj.waitingTimeSCHEDTotalExGST = convertIntoFloat(dump[-3])
                        RCTIobj.waitingTimeSCHEDTotal = convertIntoFloat(dump[-1])
                        
                    # surcharge_fixed_public_holiday
                    # surcharge_per_cubic_meters_normal
                    # surcharge_per_cubic_meters_sunday
                    # surcharge_per_cubic_meters_public_holiday

                    # others
                    # othersCost

                    # ------------------------------------------

                    RCTIobj.GSTPayable = convertIntoFloat(dump[8])
                    RCTIobj.TotalExGST = convertIntoFloat(dump[7])
                    RCTIobj.Total = convertIntoFloat(dump[9])
                    # try:
                        # print('DataList',dataList)
                    if len(dataList) <=11:
                        break
                    else:
                        dataList = dataList[11:]
                    # except :
                    #     pass
                        # print('Before Error  Solving ',len(dataList))
                        # exit()
                RCTIobj.rctiReport = rctiReportObj
                RCTIobj.save()
                
                

                # print('save')
                # print('DataList1',dataList)
                # exit()
                reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = RCTIobj.docketNumber , docketDate = RCTIobj.docketDate ).first()
                rctiTotalCost = RCTIobj.cartageTotalExGST + RCTIobj.transferKMTotalExGST + RCTIobj.returnKmTotalExGST + RCTIobj.waitingTimeSCHEDTotalExGST + RCTIobj.waitingTimeTotalExGST + RCTIobj.standByTotalExGST + RCTIobj.minimumLoadTotalExGST + RCTIobj.surchargeTotalExGST + RCTIobj.othersTotalExGST
                
                # rctiTotalCost =   RCTIobj.cartageTotal + RCTIobj.waitingTimeTotal + RCTIobj.transferKMTotal  +  RCTIobj.returnKmTotal + RCTIobj.standByTotal +RCTIobj.minimumLoadTotal
                
                if not reconciliationDocketObj :
                    reconciliationDocketObj = ReconciliationReport()
                
                reconciliationDocketObj.docketNumber =  RCTIobj.docketNumber
                reconciliationDocketObj.docketDate =  RCTIobj.docketDate
                reconciliationDocketObj.rctiLoadAndKmCost =  RCTIobj.cartageTotalExGST
                # reconciliationDocketObj.rctiSurchargeCost =   RCTIobj.docketDate
                reconciliationDocketObj.rctiWaitingTimeCost = RCTIobj.waitingTimeTotalExGST
                reconciliationDocketObj.rctiTransferKmCost = RCTIobj.transferKMTotalExGST
                reconciliationDocketObj.rctiReturnKmCost =  RCTIobj.returnKmTotalExGST
                # reconciliationDocketObj.rctiOtherCost =  RCTIobj.docketDate 
                reconciliationDocketObj.rctiStandByCost =  RCTIobj.standByTotalExGST
                reconciliationDocketObj.rctiLoadDeficit =  RCTIobj.minimumLoadTotalExGST
                reconciliationDocketObj.rctiTotalCost =  round(rctiTotalCost,2)
                reconciliationDocketObj.fromRcti = True 
                
                reconciliationDocketObj.save()
                checkMissingComponents(reconciliationDocketObj)
                
            else:
                rctiErrorObj = RctiErrors( 
                                clientName = clientName,
                                docketNumber = dataList[1],
                                docketDate = RCTIobj.docketDate,
                                errorDescription = 'To be adjusted manually by admin team',
                                fileName = fileName,
                                data = i.data
            )
                rctiErrorObj.save()

        except Exception as e:
            # print(f"Error : {e}")
            # exit()
            rctiErrorObj = RctiErrors( 
                                clientName = clientName,
                                docketNumber = RCTIobj.docketNumber,
                                docketDate = RCTIobj.docketDate,
                                errorDescription = e,
                                fileName = fileName,
                                data = i.data
            )
            rctiErrorObj.save()
            pass
