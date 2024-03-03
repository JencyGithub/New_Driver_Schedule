import csv , re
from Account_app.models import *
from Account_app.reconciliationUtils import *
import time

def convertIntoFloat(str_):
    if '(' in str_:
        str_ = '-'+str_.strip('()')
    cleaned_string = str_.replace(' ','').replace(',','')
    
    if not len(cleaned_string) > 0:
        return 0
    
    return float(cleaned_string)

def checkStr(data:str):
    return data.lower().strip().replace(" ","")

def checkDate(date_):
    pattern = r'\d{2}/\d{2}/\d{2}'
    return True if re.fullmatch(pattern,date_) else False

def dateConvert(date_):
    date_ = date_.split('/')
    year_ = '20' + date_[-1]
    return year_ + '-' + date_[1] + '-' + date_[0]

docket_pattern = r'^\d{8}$|^\d{6}$'

def reconciliationSave(docketNumber , docketDate ,clientObj ,rctiAdjustmentObj = None , RCTIobj = None):
    
    try:
        reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = docketNumber , docketDate = docketDate ).first()
        rctiTotalCost = 0
        if not reconciliationDocketObj :
            reconciliationDocketObj = ReconciliationReport()
        
            reconciliationDocketObj.docketNumber =  docketNumber
            reconciliationDocketObj.docketDate =  docketDate
            # reconciliationDocketObj.clientName =  clientNames
            reconciliationDocketObj.clientId =  clientObj.clientId
        # reconciliationDocketObj.rctiSurchargeCost =   RCTIobj.docketDate
        if rctiAdjustmentObj:
            description_ = checkStr(rctiAdjustmentObj.description)
            if  'cartage' in description_: 
                reconciliationDocketObj.rctiLoadAndKmCost += rctiAdjustmentObj.totalExGST
            elif  'waitingtime' in description_:
                reconciliationDocketObj.rctiWaitingTimeCost += rctiAdjustmentObj.totalExGST
            elif "trucktransfer" in description_:
                reconciliationDocketObj.rctiTransferKmCost += rctiAdjustmentObj.totalExGST
            elif "returnperkm" in description_:
                reconciliationDocketObj.rctiReturnKmCost += rctiAdjustmentObj.totalExGST
            elif "standbyper" in description_:
                reconciliationDocketObj.rctiStandByCost += rctiAdjustmentObj.totalExGST
            elif "minimumload" in description_:
                reconciliationDocketObj.rctiLoadDeficit += rctiAdjustmentObj.totalExGST
            rctiTotalCost = reconciliationDocketObj.rctiLoadAndKmCost + reconciliationDocketObj.rctiTransferKmCost + reconciliationDocketObj.rctiReturnKmCost + + reconciliationDocketObj.rctiWaitingTimeCost + reconciliationDocketObj.rctiStandByCost + reconciliationDocketObj.rctiLoadDeficit + reconciliationDocketObj.rctiSurchargeCost + reconciliationDocketObj.rctiOtherCost
            
        else:
            rctiTotalCost = RCTIobj.cartageTotalExGST + RCTIobj.transferKMTotalExGST + RCTIobj.returnKmTotalExGST + RCTIobj.waitingTimeSCHEDTotalExGST + RCTIobj.waitingTimeTotalExGST + RCTIobj.standByTotalExGST + RCTIobj.minimumLoadTotalExGST + RCTIobj.surchargeTotalExGST + RCTIobj.othersTotalExGST
            
            reconciliationDocketObj.rctiLoadAndKmCost =  RCTIobj.cartageTotalExGST
            
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
        reconciliationTotalCheck(reconciliationDocketObj)
        return
    except Exception as e: 
        print('Error' , e)
def insertIntoModel(dataList,file_name , data):
    RCTIobj = None
    rctiReportId = data[0]
    clientNames = data[1]
    rctiFirstDocketDate = data[2]
    rctiReportObj = RctiReport.objects.filter(pk = rctiReportId).first()
    try:
        data_str = ','.join(dataList)
        errorSolve = str(dataList) + '@_!'+ str(rctiReportId)
        rctiErrorObj = RctiErrors()
        
        # minimum Payment for top up 
        if len(dataList) == 1 and 'topup' in data_str:
            rctiErrorObj.clientName = clientNames
            rctiErrorObj.docketNumber = None
            rctiErrorObj.docketDate = None
            rctiErrorObj.errorDescription = "Manually Manage."
            rctiErrorObj.fileName = file_name.split('@_!')[-1]
            rctiErrorObj.data = str(errorSolve)
            rctiErrorObj.errorType = 1
            rctiErrorObj.save()
            return
        if len(dataList) == 1:
            rctiErrorObj.clientName = clientNames
            rctiErrorObj.docketNumber = None
            rctiErrorObj.docketDate = None
            rctiErrorObj.errorDescription = "Manually Manage."
            rctiErrorObj.fileName = file_name.split('@_!')[-1]
            rctiErrorObj.data = str(errorSolve)
            rctiErrorObj.errorType = 1
            rctiErrorObj.save()
            return
        RCTIobj =  RCTI.objects.filter(truckNo = float(dataList[0]) ,docketNumber=int(dataList[1]),docketDate = dateConvert(dataList[2])).first()

        if not RCTIobj:
            RCTIobj = RCTI()
        RCTIobj.truckNo = convertIntoFloat(dataList[0])
        clientObj = Client.objects.filter(name = clientNames).first()
        RCTIobj.clientName = clientObj
        
        
        dataList = dataList[1:]
        
        adjustmentFlag = False
        while dataList:
            if re.match(docket_pattern ,str(dataList[0])):
                RCTIobj.docketNumber = str(dataList[0])
                basePlants = BasePlant.objects.all()
                BasePlant_ = [basePlant.basePlant for basePlant in basePlants]
                description = checkStr(dataList[3])
                # if RCTIobj.docketNumber != 25652880:
                #     dataList = dataList[11:]
                #     print(dataList[0])
                #     continue
                
                RCTIobj.docketDate = dateConvert(dataList[1])
                bp = dataList[2]
                if dataList[2] not in BasePlant_:
                    i = 0
                    while len(bp) <= 10:
                        # bp = bp + dataList[3].split()
                        bp = dataList[2]
                        temp = ''
                        temp_data3 = dataList[3].split()

                        for j in range(i):
                            temp = temp + temp_data3[j] + ' '
                        temp = temp.strip()

                        bp = bp + ' ' + temp
                        if bp in BasePlant_:
                            dataList[2] = bp
                            RCTIobj.docketYard = dataList[2]
                            break
                        i = i + 1
                    else :
                        rctiErrorObj.clientName = clientNames
                        rctiErrorObj.docketNumber = RCTIobj.docketNumber
                        rctiErrorObj.docketDate = RCTIobj.docketDate
                        rctiErrorObj.errorDescription = "Earning Depot/Location does not exist."
                        rctiErrorObj.fileName = file_name
                        rctiErrorObj.data = str(errorSolve)
                        rctiErrorObj.save()
                        return
                else:
                    RCTIobj.docketYard = dataList[2] 
                # if convertIntoFloat(dataList[10]) < 0:
                # adjustmentStartDate =  '16' if rctiReportObj.reportDate.day > 15 else '01'
                # month_ = '0'+str(rctiReportObj.reportDate.month) if rctiReportObj.reportDate.month  < 10 else  str(rctiReportObj.reportDate.month)
                # date_ = str(rctiReportObj.reportDate.year)+'-'+ month_+'-'+ adjustmentStartDate
                # print(dateConvert(dataList[1]) , date_ , dateConvert(dataList[1])  < date_ , dataList)
                if dateConvert(dataList[1])  < rctiFirstDocketDate:
                    adjustmentFlag = True
                    rctiAdjustmentObj = RctiAdjustment()
                    rctiAdjustmentObj.truckNo = RCTIobj.truckNo
                    rctiAdjustmentObj.docketNumber = dataList[0]
                    rctiAdjustmentObj.docketDate = dateConvert(dataList[1])
                    rctiAdjustmentObj.docketYard = dataList[2]
                    rctiAdjustmentObj.clientName = RCTIobj.clientName
                    rctiAdjustmentObj.rctiReport = rctiReportObj
                    rctiAdjustmentObj.description = dataList[3]
                    rctiAdjustmentObj.noOfKm = convertIntoFloat(dataList[4])
                    rctiAdjustmentObj.invoiceQuantity = convertIntoFloat(dataList[5])
                    rctiAdjustmentObj.unit = dataList[6]
                    rctiAdjustmentObj.unitPrice = convertIntoFloat(dataList[7])
                    rctiAdjustmentObj.totalExGST = convertIntoFloat(dataList[8])
                    rctiAdjustmentObj.GSTPayable = convertIntoFloat(dataList[9])
                    rctiAdjustmentObj.Total = convertIntoFloat(dataList[10])
                    rctiAdjustmentObj.save()
                    reconciliationSave(rctiAdjustmentObj.docketNumber , rctiAdjustmentObj.docketDate ,clientObj , rctiAdjustmentObj = rctiAdjustmentObj)
                    
                elif "trucktransfer" in description:
                    RCTIobj.transferKM = convertIntoFloat(dataList[5])
                    RCTIobj.transferKMCost = convertIntoFloat(dataList[7])
                    RCTIobj.transferKMTotalExGST = convertIntoFloat(dataList[8])
                    RCTIobj.transferKMGSTPayable = convertIntoFloat(dataList[9])
                    RCTIobj.transferKMTotal = convertIntoFloat(dataList[10])
                elif "cartage" in description:
                    RCTIobj.noOfKm = convertIntoFloat(dataList[4])
                    RCTIobj.cubicMl = convertIntoFloat(dataList[5])
                    RCTIobj.cubicMiAndKmsCost = convertIntoFloat(dataList[7])
                    RCTIobj.destination = dataList[3].split('CARTAGE')[0]
                    RCTIobj.cartageTotalExGST = convertIntoFloat(dataList[8])
                    RCTIobj.cartageGSTPayable = convertIntoFloat(dataList[9])
                    RCTIobj.cartageTotal = convertIntoFloat(dataList[10])
                elif "returnperkm" in description:
                    RCTIobj.returnKm = convertIntoFloat(dataList[5])
                    RCTIobj.returnPerKmPerCubicMeterCost = convertIntoFloat(dataList[7])
                    RCTIobj.returnKmTotalExGST = convertIntoFloat(dataList[8])
                    RCTIobj.returnKmGSTPayable = convertIntoFloat(dataList[9])
                    RCTIobj.returnKmTotal = convertIntoFloat(dataList[10])
                elif "waitingtimesched" in description:
                    RCTIobj.waitingTimeSCHED = convertIntoFloat(dataList[5])
                    RCTIobj.waitingTimeSCHEDCost = convertIntoFloat(dataList[7])
                    RCTIobj.waitingTimeSCHEDTotalExGST = convertIntoFloat(dataList[8])
                    RCTIobj.waitingTimeSCHEDGSTPayable = convertIntoFloat(dataList[9])
                    RCTIobj.waitingTimeSCHEDTotal = convertIntoFloat(dataList[10])
                elif "waitingtime" in description:
                    RCTIobj.waitingTimeInMinutes = convertIntoFloat(dataList[5])
                    RCTIobj.waitingTimeCost = convertIntoFloat(dataList[7])
                    RCTIobj.waitingTimeTotalExGST = convertIntoFloat(dataList[8])
                    RCTIobj.waitingTimeGSTPayable = convertIntoFloat(dataList[9])
                    RCTIobj.waitingTimeTotal = convertIntoFloat(dataList[10])
                elif "minimumload" in description:
                    RCTIobj.minimumLoad = convertIntoFloat(dataList[5])
                    RCTIobj.loadCost = convertIntoFloat(dataList[7])
                    RCTIobj.minimumLoadTotalExGST = convertIntoFloat(dataList[8])
                    RCTIobj.minimumLoadGSTPayable = convertIntoFloat(dataList[9])
                    RCTIobj.minimumLoadTotal = convertIntoFloat(dataList[10])
                elif "standbyper" in description:
                    RCTIobj.standByNoSlot = convertIntoFloat(dataList[5])
                    RCTIobj.standByUnit = 'slot' if str(dataList[6].lower()) == 'each' else 'minute'
                    RCTIobj.standByPerHalfHourDuration = convertIntoFloat(dataList[7])
                    RCTIobj.standByTotalExGST = convertIntoFloat(dataList[8])
                    RCTIobj.standByGSTPayable = convertIntoFloat(dataList[9])
                    RCTIobj.standByTotal = convertIntoFloat(dataList[10])
                elif "surcharge" in description:
                    RCTIobj.surcharge = convertIntoFloat(dataList[5])
                    RCTIobj.surchargeCost = convertIntoFloat(dataList[7])
                    RCTIobj.surchargeTotalExGST = convertIntoFloat(dataList[8])
                    RCTIobj.surchargeGSTPayable = convertIntoFloat(dataList[9])
                    RCTIobj.surchargeTotal = convertIntoFloat(dataList[10])
                
                else:
                    RCTIobj.otherDescription += dataList[3]
                    RCTIobj.others = RCTIobj.others + convertIntoFloat(dataList[5])
                    RCTIobj.othersCost = RCTIobj.othersCost + convertIntoFloat(dataList[7])
                    RCTIobj.othersGSTPayable = RCTIobj.othersGSTPayable + convertIntoFloat(dataList[8])
                    RCTIobj.othersTotalExGST = RCTIobj.othersTotalExGST + convertIntoFloat(dataList[9])
                    RCTIobj.othersTotal =  RCTIobj.othersTotal +convertIntoFloat(dataList[10])
                    
                
                dataList = dataList[11:]
        if not adjustmentFlag :
            RCTIobj.rctiReport = rctiReportObj
            RCTIobj.save()
            reconciliationSave(RCTIobj.docketNumber , RCTIobj.docketDate ,clientObj , RCTIobj = RCTIobj)
    except Exception as e:
        
        rctiErrorObj.clientName = clientNames
        rctiErrorObj.docketNumber = dataList[0]
        rctiErrorObj.docketDate =  dataList[1]
        rctiErrorObj.errorDescription = e
        rctiErrorObj.fileName = file_name
        rctiErrorObj.data = str(errorSolve)
        rctiErrorObj.save() 
        pass

def insertIntoExpenseModel(dataList , file_name,data):
    errorSolve = dataList
    clientNames = data[1]
    if dataList:
        try:
            rctiExpenseObj = RctiExpense()
            if checkDate(dataList[2]):
                clientNameObj = Client.objects.filter(name = clientNames).first()
                rctiExpenseObj.clientName  = clientNameObj
                rctiExpenseObj.truckNo = str(dataList[0])
                rctiExpenseObj.docketNumber = str(dataList[1])
                rctiExpenseObj.docketDate = dateConvert(dataList[2])
                rctiExpenseObj.docketYard = str(dataList[3]).upper()
                rctiExpenseObj.description = str(dataList[4])
                rctiExpenseObj.paidKm =  0
                rctiExpenseObj.invoiceQuantity =  convertIntoFloat(dataList[5])
                rctiExpenseObj.unit =  dataList[6]
                rctiExpenseObj.unitPrice =  convertIntoFloat(dataList[7])
                rctiExpenseObj.totalExGST =  convertIntoFloat(dataList[8])
                rctiExpenseObj.gstPayable =  convertIntoFloat(dataList[9])
                rctiExpenseObj.total =  convertIntoFloat(dataList[10])
                rctiExpenseObj.save()
                return
        except Exception as e:
            rctiErrorObj = RctiErrors() 
            rctiErrorObj.clientName = clientNames
            rctiErrorObj.docketNumber = dataList[1]
            rctiErrorObj.docketDate =  dataList[2]
            rctiErrorObj.errorDescription = 'expense' + e
            rctiErrorObj.fileName = file_name
            rctiErrorObj.data = str(errorSolve)
            rctiErrorObj.save() 
            return           
    else:
        with open('csvToModelSkip.txt','a')as f:
            f.write('expenses' + file_name + str(dataList)+'\n')
        return
       
       
with open("File_name_file.txt", 'r') as f:
    file_names = f.read().split('<>')   
            
with open("rctiReportId.txt", 'r') as f:
    data = f.read().split(',')
 
    
earningFileName = file_names[0].strip()
expenseFileName = file_names[1].strip()

try:
    earningFile = open(f'static/Account/RCTI/RCTIInvoice/{earningFileName}', 'r')
    earningReader = csv.reader(earningFile)
    for earningData in earningReader:
        insertIntoModel(earningData,earningFileName,data)      

except Exception as e:
    with open ('Earning_error.txt','a') as f:
        f.write(str(e))

try:
    expenseFile = open(f'static/Account/RCTI/RCTIInvoice/{expenseFileName}', 'r')
    expenseReader = csv.reader(expenseFile)
    for expenseData in expenseReader:
        insertIntoExpenseModel(expenseData,expenseFileName,data)
except Exception as e:
    with open ('Expense_error.txt','a') as f:
        f.write(str(e))