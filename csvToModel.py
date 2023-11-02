import csv
from Account_app.models import *
from Account_app.reconciliationUtils import *



def dateConvert(date_):
    date_ = date_.split('/')
    year_ = '20' + date_[-1]
    return year_ + '-' + date_[1] + '-' + date_[0]

def insertTopUpRecord(list_):
    RCTIobj = RCTI()
    excistingRCTI = RCTI.objects.filter(docketDate = dateConvert(list_[1].split()[-1]) , docketNumber = list_[1].split()[0]).first()
    if not  excistingRCTI :
        RCTIobj.docketDate = dateConvert(list_[1].split()[-1])
        RCTIobj.docketNumber = list_[1].split()[0]
        # RCTIobj.docketNumber = 1
        RCTIobj.others = list_[2]
        RCTIobj.othersCost = float(list_[6].replace(' ',''))
        RCTIobj.docketYard = ' '
        RCTIobj.save()

    return

def insertIntoModel(dataList,file_name):
    
    try:
        RCTIobj = None
        try:
            existingDocket = RCTI.objects.get( docketNumber=int(dataList[1]))
            if str(existingDocket.docketDate) == dateConvert(dataList[2]):
                RCTIobj = existingDocket
        except:
            RCTIobj = RCTI()
    
        RCTIobj.truckNo = float(dataList[0])
        RCTIobj.docketNumber = int(dataList[1])
        dataList = dataList[2:]

        while dataList:

            dump = dataList[:10]
            description = dump[2].lower().strip()
            if 'top up' in description:
                insertTopUpRecord(dataList)
                dataList = dataList[10:]
                continue
                
            RCTIobj.docketDate = dateConvert(dump[0])
            RCTIobj.docketYard = dump[1]
            if "truck transfer" in description:
                RCTIobj.transferKM = float(dump[4])
                RCTIobj.transferKMCost = float(dump[6])
                RCTIobj.transferKMGSTPayable = float(dump[-2])
                RCTIobj.transferKMTotalExGST = float(dump[-3])
                RCTIobj.transferKMTotal = float(dump[-1])
            elif "cartage" in description:
                RCTIobj.noOfKm = float(dump[3])
                RCTIobj.cubicMl = float(dump[4])
                RCTIobj.cubicMiAndKmsCost = float(dump[6])
                RCTIobj.destination = description.split('cartage')[0]
                RCTIobj.cartageGSTPayable = float(dump[-2])
                RCTIobj.cartageTotalExGST = float(dump[-3])
                RCTIobj.cartageTotal = float(dump[-1])
            elif "return" in description:
                RCTIobj.returnKm = float(dump[4])
                RCTIobj.returnPerKmPerCubicMeterCost = float(dump[6])
                RCTIobj.returnKmGSTPayable = float(dump[-2])
                RCTIobj.returnKmTotalExGST = float(dump[-3])
                RCTIobj.returnKmTotal = float(dump[-1])
            elif "waiting time" in description:
                RCTIobj.waitingTimeInMinutes = float(dump[4])
                RCTIobj.waitingTimeCost = float(dump[6])
                RCTIobj.waitingTimeGSTPayable = float(dump[-2])
                RCTIobj.waitingTimeTotalExGST = float(dump[-3])
                RCTIobj.waitingTimeTotal = float(dump[-1])
            elif "minimum load" in description:
                RCTIobj.minimumLoad = float(dump[4])
                RCTIobj.loadCost = float(dump[6])
                RCTIobj.minimumLoadGSTPayable = float(dump[-2])
                RCTIobj.minimumLoadTotalExGST = float(dump[-3])
                RCTIobj.minimumLoadTotal = float(dump[-1])
            elif "standby" in description:
                RCTIobj.standByPerHalfHourCost = float(dump[4])
                RCTIobj.standByUnit = 'slot' if str(
                    dump[5].lower()) == 'each' else 'minute'
                RCTIobj.standByPerHalfHourDuration = float(dump[6])
                RCTIobj.standByGSTPayable = float(dump[-2])
                RCTIobj.standByTotalExGST = float(dump[-3])
                RCTIobj.standByTotal = float(dump[-1])
            elif "surcharge after hours" in description:
                RCTIobj.surcharge_duration = float(dump[4])
                if "mon-fri" in description and "each" in str(dump[5].lower()):
                    RCTIobj.surcharge_fixed_normal = float(dump[6])
                elif "sat" in description and 'mon' in description and "each" in str(dump[5].lower()):
                    RCTIobj.surcharge_fixed_sunday = float(dump[6])
                RCTIobj.surchargeGSTPayable = float(dump[-2])
                RCTIobj.surchargeTotalExGST = float(dump[-3])
                RCTIobj.surchargeTotal = float(dump[-1])
            elif "waiting time sched" in description:
                RCTIobj.waitingTimeSCHED = float(dump[4])
                RCTIobj.waitingTimeSCHEDCost = float(dump[6])
                RCTIobj.waitingTimeSCHEDGSTPayable = float(dump[-2])
                RCTIobj.waitingTimeSCHEDTotalExGST = float(dump[-3])
                RCTIobj.waitingTimeSCHEDTotal = float(dump[-1])
                
                
            # surcharge_fixed_public_holiday
            # surcharge_per_cubic_meters_normal
            # surcharge_per_cubic_meters_sunday
            # surcharge_per_cubic_meters_public_holiday

            # others
            # othersCost

            # ------------------------------------------

            RCTIobj.GSTPayable = float(dump[8])
            RCTIobj.TotalExGST = float(dump[7])
            RCTIobj.Total = float(dump[9])

            dataList = dataList[10:]
        RCTIobj.save()
        
        reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = RCTIobj.docketNumber , docketDate = RCTIobj.docketDate ).first()
        
        rctiTotalCost =   RCTIobj.cartageTotal + RCTIobj.waitingTimeTotal + RCTIobj.transferKMTotal  +  RCTIobj.returnKmTotal + RCTIobj.standByTotal +RCTIobj.minimumLoadTotal
        
        if not  reconciliationDocketObj :
            reconciliationDocketObj = ReconciliationReport()
        
        reconciliationDocketObj.docketNumber =  RCTIobj.docketNumber
        reconciliationDocketObj.docketDate =  RCTIobj.docketDate
        reconciliationDocketObj.rctiLoadAndKmCost =  RCTIobj.cartageTotal
        # reconciliationDocketObj.rctiSurchargeCost =   RCTIobj.docketDate
        reconciliationDocketObj.rctiWaitingTimeCost = RCTIobj.waitingTimeTotal  
        reconciliationDocketObj.rctiTransferKmCost = RCTIobj.transferKMTotal 
        reconciliationDocketObj.rctiReturnKmCost =  RCTIobj.returnKmTotal
        # reconciliationDocketObj.rctiOtherCost =  RCTIobj.docketDate 
        reconciliationDocketObj.rctiStandByCost =  RCTIobj.standByTotal
        reconciliationDocketObj.rctiLoadDeficit =  RCTIobj.minimumLoadTotal
        reconciliationDocketObj.rctiTotalCost =  round(rctiTotalCost,2)
        reconciliationDocketObj.fromRcti = True 
        
        reconciliationDocketObj.save()
        checkMissingComponents(reconciliationDocketObj)
        
        
        # exit()

    except Exception as e:
        # print(f"Error : {e}")
        rctiErrorObj = RctiErrors( 
                            docketNumber = RCTIobj.docketNumber,
                            docketDate = RCTIobj.docketDate,
                            errorDescription = e,
                            fileName = file_name
        )
        rctiErrorObj.save()
        # print(f' Docket No :{RCTIobj.docketNumber}. Docket Date : {RCTIobj.docketDate}  , Error : {e} \n {dataList} \n\n\n')
        # exit()
        pass


        # exit()
        
f = open("File_name_file.txt", 'r')
file_name = f.read()
# file_name = 'converted_20231030113104@_!pdf1.csv'
convertFileName = file_name.split('@_!')[1]

files = open(f'static/Account/RCTI/RCTIInvoice/{file_name}', 'r')
reader = csv.reader(files)
next(reader)
# for key,row in reader.iterrows():
#     try:
#         insertIntoModel(row,key)
#     except Exception as e:
#         print(f" ! Error : {e}")
for row in reader:
    insertIntoModel(row,convertFileName)
