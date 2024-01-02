import csv , re
from Account_app.models import *
from Account_app.reconciliationUtils import *
import time

def convertIntoFloat(str_):
    if '(' in str_:
        str_ = '-'+str_.strip('()')
    cleaned_string = str_.replace(' ','').replace(',','')
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


def insertIntoModel(dataList,file_name):
    RCTIobj = None
    try:
        data_str = ','.join(dataList)
        errorSolve = dataList
        rctiErrorObj = RctiErrors()
        
        if 'topup' in (data_str).strip().lower().replace(' ',''):
            rctiErrorObj.clientName = 'boral'
            rctiErrorObj.docketNumber = None
            rctiErrorObj.docketDate = None
            rctiErrorObj.errorDescription = "Manage Top-up."
            rctiErrorObj.fileName = file_name
            rctiErrorObj.data = str(errorSolve)
            rctiErrorObj.save()
            return
        if 'tolls' in (data_str).strip().lower().replace(' ',''):
            rctiErrorObj.clientName = 'boral'
            rctiErrorObj.docketNumber = None
            rctiErrorObj.docketDate = None
            rctiErrorObj.errorDescription = "Manage Tolls."
            rctiErrorObj.fileName = file_name
            rctiErrorObj.data = str(errorSolve)
            rctiErrorObj.save()
            return

        RCTIobj =  RCTI.objects.filter(truckNo = float(dataList[0]) ,docketNumber=int(dataList[1]),docketDate = dateConvert(dataList[2])).first()

        if not RCTIobj:
            RCTIobj = RCTI()
        RCTIobj.truckNo = convertIntoFloat(dataList[0])
        RCTIobj.clientName = Client.objects.filter(name = 'boral').first()
        
        
        dataList = dataList[1:]
        
        
        while dataList:
            if re.match(docket_pattern ,str(dataList[0])):
                RCTIobj.docketNumber = str(dataList[0])
                basePlants = BasePlant.objects.all()
                BasePlant_ = [basePlant.basePlant for basePlant in basePlants]
                description = checkStr(dataList[3])
                                    
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
                            # print(RCTIobj.docketNumber,RCTIobj.docketYard)
                            break
                        i = i + 1
                    else :
                        rctiErrorObj.clientName = 'boral'
                        rctiErrorObj.docketNumber = RCTIobj.docketNumber
                        rctiErrorObj.docketDate = RCTIobj.docketDate
                        rctiErrorObj.errorDescription = "Earning Depot/Location does not exist."
                        rctiErrorObj.fileName = file_name
                        rctiErrorObj.data = str(errorSolve)
                        rctiErrorObj.save()
                        return
                else:
                    RCTIobj.docketYard = dataList[2] 
                
                if "trucktransfer" in description:
                    RCTIobj.transferKM = convertIntoFloat(dataList[5])
                    RCTIobj.transferKMCost = convertIntoFloat(dataList[7])
                    RCTIobj.transferKMTotalExGST = convertIntoFloat(dataList[8])
                    RCTIobj.transferKMGSTPayable = convertIntoFloat(dataList[9])
                    RCTIobj.transferKMTotal = convertIntoFloat(dataList[10])
                elif "cartage" in description:
                    RCTIobj.noOfKm = convertIntoFloat(dataList[4])
                    RCTIobj.cubicMl = convertIntoFloat(dataList[5])
                    RCTIobj.cubicMiAndKmsCost = convertIntoFloat(dataList[7])
                    RCTIobj.destination = description.split('cartage')[0]
                    RCTIobj.cartageTotalExGST = convertIntoFloat(dataList[8])
                    RCTIobj.cartageGSTPayable = convertIntoFloat(dataList[9])
                    RCTIobj.cartageTotal = convertIntoFloat(dataList[10])
                elif "returnperkm" in description:
                    RCTIobj.returnKm = convertIntoFloat(dataList[5])
                    RCTIobj.returnPerKmPerCubicMeterCost = convertIntoFloat(dataList[7])
                    RCTIobj.returnKmTotalExGST = convertIntoFloat(dataList[8])
                    RCTIobj.returnKmGSTPayable = convertIntoFloat(dataList[9])
                    RCTIobj.returnKmTotal = convertIntoFloat(dataList[10])
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
                elif "waitingtimesched" in description:
                    RCTIobj.waitingTimeSCHED = convertIntoFloat(dataList[5])
                    RCTIobj.waitingTimeSCHEDCost = convertIntoFloat(dataList[7])
                    RCTIobj.waitingTimeSCHEDTotalExGST = convertIntoFloat(dataList[8])
                    RCTIobj.waitingTimeSCHEDGSTPayable = convertIntoFloat(dataList[9])
                    RCTIobj.waitingTimeSCHEDTotal = convertIntoFloat(dataList[10])
                else:
                    with open('csvToModelSkip.txt','a')as f:
                        f.write('earnings' + file_name + str(dataList)+'\n')
                dataList = dataList[11:]
            
        RCTIobj.save()
            
        reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = RCTIobj.docketNumber , docketDate = RCTIobj.docketDate ).first()
        rctiTotalCost = RCTIobj.cartageTotalExGST + RCTIobj.transferKMTotalExGST + RCTIobj.returnKmTotalExGST + RCTIobj.waitingTimeSCHEDTotalExGST + RCTIobj.waitingTimeTotalExGST + RCTIobj.standByTotalExGST + RCTIobj.minimumLoadTotalExGST + RCTIobj.surchargeTotalExGST + RCTIobj.othersTotalExGST

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
        return

    except Exception as e:
        rctiErrorObj.clientName = 'boral'
        rctiErrorObj.docketNumber = dataList[1]
        rctiErrorObj.docketDate =  dataList[2]
        rctiErrorObj.errorDescription = e
        rctiErrorObj.fileName = file_name
        rctiErrorObj.data = str(errorSolve)
        rctiErrorObj.save() 
        pass

def insertIntoExpenseModel(dataList , file_name):
    errorSolve = dataList
    if dataList:
        try:
            rctiExpenseObj = RctiExpense()
            if checkDate(dataList[2]):
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
            rctiErrorObj.clientName = 'boral'
            rctiErrorObj.docketNumber = dataList[1]
            rctiErrorObj.docketDate =  dataList[2]
            rctiErrorObj.errorDescription = e
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
            
earningFileName = file_names[0].strip()
expenseFileName = file_names[1].strip()

try:
    earningFile = open(f'static/Account/RCTI/RCTIInvoice/{earningFileName}', 'r')
    earningReader = csv.reader(earningFile)
    for earningData in earningReader:
        insertIntoModel(earningData,earningFileName)      

except Exception as e:
    with open ('Earning_error.txt','a') as f:
        f.write(str(e))

try:
    expenseFile = open(f'static/Account/RCTI/RCTIInvoice/{expenseFileName}', 'r')
    expenseReader = csv.reader(expenseFile)
    for expenseData in expenseReader:
        insertIntoExpenseModel(expenseData,expenseFileName)
except Exception as e:
    with open ('Expense_error.txt','a') as f:
        f.write(str(e))