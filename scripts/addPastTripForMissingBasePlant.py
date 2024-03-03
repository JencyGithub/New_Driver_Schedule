from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
from Account_app.reconciliationUtils import  *
from datetime import time
import csv , re
from variables import *
from utils import *

f = open(r"scripts/addPastTripForMissingBasePlant.txt", 'r')
basePlantName = f.read()

matchingData = PastTripError.objects.filter(errorFromPastTrip="BasePlant does not exist.", status=False)

# For PastTrip 
tripIdList = set()
for i in matchingData:
    
    res = ''
    try:
        data = i.data
        data = data.replace('[','').replace(']','').replace('\\n','').replace("'",'')
        data = data.split(',')
        for j in range(len(data)):
            data[j] = data[j].strip()
        if ' ' in str(data[0].strip()):
            res_ = str(data[0].strip()).split()[0]
        elif '/' in str(data[0].strip()):
            str_ = str(data[0].strip()).split('/')
            res_ = str_[-1]+'-'+str_[-2]+'-'+str_[0]
        else:
            res_ = str(data[0].strip())

        
        pastBasePlant = data[24].strip().upper()

                
        

        basePlant = BasePlant.objects.filter(basePlant = basePlantName).first()
        
        if pastBasePlant.upper().strip() == basePlant.basePlant.upper().strip():
            i.status = True
            i.save()
            shiftDate = datetime.strptime(res_, '%Y-%m-%d')
            startTime = datetime.strptime(str(data[6]), '%H:%M:%S').time()
            startTimeDateTime = datetime.combine(shiftDate.date(), startTime)

            endTime = datetime.strptime(str(data[7]), '%H:%M:%S').time()
            endTimeDateTime = datetime.combine(shiftDate.date(),endTime)
            clientObj = Client.objects.filter(name = i.clientName).first()
            driverObj = Driver.objects.filter(driverId=int(data[4].strip())).first()

            tripObjGet = saveDate(driverObj = driverObj ,clientObj = clientObj ,data = data ,shiftDate = shiftDate ,startTimeDateTime =startTimeDateTime , endTimeDateTime = endTimeDateTime  , clientName_= i.clientName, fileName =i.fileName.split('@_!')[-1] ,res_ =res_,count_ =i.lineNumber)
            if tripObjGet:
                tripIdList.add(tripObjGet.id)


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


try:
    tripObjList = DriverShiftTrip.objects.filter(pk__in = tripIdList)
    checkShiftRevenueDifference(tripObjList=tripObjList)
except Exception as e:
    pass

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
