import csv , re
from Account_app.models import *
from Account_app.reconciliationUtils import *
import time

def convertIntoFloat(str_):
    if '(' in str_:
        str_ = '-'+str_.strip('()')
    cleaned_string = str_.replace(' ','').replace(',','')
    return float(cleaned_string)


def checkDate(date_):
    pattern = r'\d{2}/\d{2}/\d{2}'
    return True if re.fullmatch(pattern,date_) else False

def dateConvert(date_):
    date_ = date_.split('/')
    year_ = '20' + date_[-1]
    return year_ + '-' + date_[1] + '-' + date_[0]

def insertTopUpRecord(list_, truckNo, docketNumber):
    RCTIobj = RCTI()
    excistingRCTI = RCTI.objects.filter(docketDate = dateConvert(list_[0].split()[-1]) , docketNumber = docketNumber).first()
    if not excistingRCTI :
        RCTIobj.docketNumber = docketNumber
        RCTIobj.truckNo = truckNo
    RCTIobj.docketDate = dateConvert(list_[0].split()[-1])
    RCTIobj.docketYard = list_[1]
    
    RCTIobj.others = list_[2]
    RCTIobj.othersCost = convertIntoFloat(list_[6])
    RCTIobj.othersGSTPayable = list_[7]
    RCTIobj.othersTotalExGST = list_[8]
    RCTIobj.othersTotal = list_[9]
    # RCTIobj.save()
    return RCTIobj

docket_pattern = r'^\d{8}$|^\d{6}$'


def insertIntoModel(dataList,file_name):
    try:
        
        errorSolve = dataList
        # if 'adjustmen' != str(dataList[1]).strip().lower():
        RCTIobj =  RCTI.objects.filter(docketNumber=dataList[1],docketDate = dateConvert(dataList[2])).first()
        if not RCTIobj:
            RCTIobj = RCTI()

        RCTIobj.truckNo = convertIntoFloat(dataList[0])
        RCTIobj.clientName = Client.objects.filter(name = 'boral').first()
        if re.match(docket_pattern ,str(dataList[1])) or 'adjustmen' == str(dataList[1]).strip().lower():

            RCTIobj.docketNumber = str(dataList[1])
            dataList = dataList[2:]
            basePlants = BasePlant.objects.all()
            BasePlant_ = [basePlant.basePlant for basePlant in basePlants]
            
            while dataList:

                dump = dataList[:10]
                description = dump[2].lower().strip()
                
                if 'top up' in description:
                    # insertTopUpRecord(dump, RCTIobj.truckNo, RCTIobj.docketNumber)
                    # RCTIobj.docketDate = dateConvert(dump[0].split()[-1])
                    # RCTIobj.docketYard = dump[1]
                    
                    # RCTIobj.others = dump[2]
                    # RCTIobj.othersCost = convertIntoFloat(dump[6])
                    # RCTIobj.othersGSTPayable = convertIntoFloat(dump[7])
                    # RCTIobj.othersTotalExGST = convertIntoFloat(dump[8])
                    # RCTIobj.othersTotal = convertIntoFloat(dump[9])
                    # dataList = dataList[10:]
                    rctiErrorObj = RctiErrors( 
                                        clientName = 'boral',
                                        docketNumber = RCTIobj.docketNumber,
                                        docketDate = RCTIobj.docketDate,
                                        errorDescription = "Manage Top-up.",
                                        fileName = file_name,
                                        data = str(errorSolve)
                    )
                    rctiErrorObj.save()
                    return

                    
                RCTIobj.docketDate = dateConvert(dump[0])
                if dump[1] not in BasePlant_:
                    rctiErrorObj = RctiErrors( 
                                        clientName = 'boral',
                                        docketNumber = RCTIobj.docketNumber,
                                        docketDate = RCTIobj.docketDate,
                                        errorDescription = "Earning Depot/Location does not exist.",
                                        fileName = file_name,
                                        data = str(errorSolve)
                    )
                    rctiErrorObj.save()
                    dataList = dataList[10:]
                    return
                else:
                    # BasePlant_ = BasePlant.objects.filter(basePlant = str(dump[1]).upper()).first()
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
                # elif "surcharge after hours" in description:
                #     RCTIobj.surcharge_duration = convertIntoFloat(dump[4])
                #     if "mon-fri" in description and "each" in str(dump[5].lower()):
                #         RCTIobj.surcharge_fixed_normal = convertIntoFloat(dump[6])
                #     elif "sat" in description and 'mon' in description and "each" in str(dump[5].lower()):
                #         RCTIobj.surcharge_fixed_sunday = convertIntoFloat(dump[6])
                #     RCTIobj.surchargeGSTPayable = convertIntoFloat(dump[-2])
                #     RCTIobj.surchargeTotalExGST = convertIntoFloat(dump[-3])
                #     RCTIobj.surchargeTotal = convertIntoFloat(dump[-1])

                elif "surcharge" in description:
                    RCTIobj.surcharge = convertIntoFloat(dump[4])
                    RCTIobj.surchargeCost = convertIntoFloat(dump[6])
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

                dataList = dataList[10:]
            RCTIobj.save()
            
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
                            clientName = 'boral',
                            docketNumber = dataList[1],
                            docketDate = RCTIobj.docketDate,
                            errorDescription = 'To be adjusted manually by admin team',
                            fileName = file_name,
                            data = str(errorSolve)
        )
            rctiErrorObj.save()

    except Exception as e:
        rctiErrorObj = RctiErrors( 
                            clientName = 'boral',
                            docketNumber = RCTIobj.docketNumber,
                            docketDate = RCTIobj.docketDate,
                            errorDescription = e,
                            fileName = file_name,
                            data = str(errorSolve)
        )
        rctiErrorObj.save()
        pass

def insertIntoExpenseModel(dataList , file_name):
    errorSolve = dataList
    basePlants = BasePlant.objects.all()
    BasePlant_ = [basePlant.basePlant for basePlant in basePlants]
    if dataList and len(dataList) > 10:
        try:
            rctiExpenseObj = RctiExpense()
            if checkDate(dataList[2]):
                rctiExpenseObj.truckNo = str(dataList[0])
                rctiExpenseObj.docketNumber = str(dataList[1])
                rctiExpenseObj.docketDate = dateConvert(dataList[2])
                
                # if dataList[2] is not BasePlant_:
                #     BasePlant_ = BasePlant.objects.get_or_create(basePlant = str(dataList[3]).upper())[0]

                # if dataList[3] not in  BasePlant_:
                #     rctiErrorObj = RctiErrors( 
                #                         docketNumber = rctiExpenseObj.docketNumber,
                #                         docketDate = rctiExpenseObj.docketDate,
                #                         errorDescription = "Expense Depot/Location does not exist.",
                #                         fileName = file_name,
                #                         data = str(dataList))
                #     rctiErrorObj.save()
                #     pass
                # else:
                #     BasePlant_ = BasePlant.objects.filter(basePlant = str(dataList[1]).upper()).first()

                rctiExpenseObj.docketYard = str(dataList[3]).upper()
                rctiExpenseObj.description = str(dataList[4])
                rctiExpenseObj.paidKm =  0
                rctiExpenseObj.invoiceQuantity =  convertIntoFloat(dataList[6])
                rctiExpenseObj.unit =  dataList[7]
                rctiExpenseObj.unitPrice =  convertIntoFloat(dataList[8])
                rctiExpenseObj.gstPayable =  convertIntoFloat(dataList[9])
                rctiExpenseObj.totalExGST =  convertIntoFloat(dataList[10])
                rctiExpenseObj.total =  convertIntoFloat(dataList[11])
                rctiExpenseObj.save()
        except Exception as e:
            rctiErrorObj = RctiErrors( 
                            docketNumber = rctiExpenseObj.docketNumber,
                            docketDate = rctiExpenseObj.docketDate,
                            errorDescription = e,
                            fileName = file_name,
                            data = str(errorSolve)
            )
            rctiErrorObj.save()
            
try:
    with open("File_name_file.txt", 'r') as f:
        file_name = f.read()
    # file_name = file_name.strip()
    file_name = file_name.split('<>')
    
    # file_name = 'converted_20231030113104@_!pdf1.csv'
    convertFileName = file_name[0].split('@_!')[1]

    file = open(f'static/Account/RCTI/RCTIInvoice/{file_name[0].strip()}', 'r')
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        insertIntoModel(row,convertFileName)

    # Expense 
    fileExpense = open(f'static/Account/RCTI/RCTIInvoice/{file_name[1].strip()}', 'r')
    reader = csv.reader(fileExpense)
    for row in reader:
        insertIntoExpenseModel(row , convertFileName)
        
except Exception as e:
    with open ('Expense_error.txt','a') as f:
        f.write(str(e))
