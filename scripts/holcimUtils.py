import re,csv
from Account_app.models import *
from GearBox_app.models import *
from Appointment_app.models import *
from datetime import datetime
from Account_app.reconciliationUtils import *



def checkStr(data:str):
    return data.lower().strip().replace(" ","")
rctiReportId = None
with open("rctiReportId.txt", 'r') as f:
    data = f.read().split(',')

    rctiReportId = data[0] 
    clientName = Client.objects.filter(name = str(data[1])).first()
fileName = None
with open('File_name_file.txt','r')as f:
    fileName = f.read()
    

def convertIntoFloat(str_):
    if '(' in str_:
        str_ = '-'+str_.strip('()')
    cleaned_string = str_.replace(' ','').replace(',','')
    
    if not len(cleaned_string) > 0:
        return 0
    
    return float(cleaned_string)

def checkStr(data:str):
    return data.lower().strip().replace(" ","")
    
manuallyManaged = ["creekpayment","accommodation","topup","ampol","inspectionfailure","diwalisweets","missingdocketpayment"]

with open('holcimUtils.txt', 'w') as file:
    pass 
with open('holcim.txt', 'w') as file:
    pass 


with open(f'static/Account/RCTI/RCTIInvoice/{fileName}','r') as f:
    csv_reader = csv.reader(f)
    rctiErrorObj = RctiErrors()
    finalList = []
    prepared = []
    tempData = []
    lineCount = 0
    datePattern = r'\d{2}\.\d{2}\.\d{4}'
    
    docketPattern = r'(\d{5,11}[a-zA-Z]{0,2})'
    docketPattern2 = r'(^G-\d{6})'

    truckNo = None
    total = 0
    fileDetails = []
    rctiRepoort = None
    flag = False
    strValue = ''
    rowErrorDescription = ''
    
    try:
        for row in csv_reader:
            
            lineCount += 1
            errorSolve = str(row) + '@_!'+ str(rctiReportId)
            if row[0].strip() in '':
                continue
            if '@' in row[0]:
                row[0]=row[0].replace(' @ ','@')
            splitRow = row[0].split()
            splitRow = list(filter(lambda x: x.strip() != '', splitRow))
            if 'paymentfortruck' in checkStr(row[0]):
                truckNo = row[0].split(',')[-3]
                
                # for docket pattern = 'G-111111'
            elif  re.fullmatch(datePattern, splitRow[0].strip()) and  re.fullmatch(docketPattern2, str(splitRow[1].strip())) :
                rctiErrorObj = RctiErrors()
                rctiErrorObj.clientName = clientName.id
                rctiErrorObj.docketNumber = None
                rctiErrorObj.docketDate = None
                rctiErrorObj.errorDescription = "Manually Manage."
                rctiErrorObj.fileName = fileName.split('@_!')[-1]
                rctiErrorObj.data = str(errorSolve)
                # rctiErrorObj.errorType = 1
                rctiErrorObj.save()
                
                # for top up in docketnumber  
            elif  re.fullmatch(datePattern, splitRow[0].strip()) and  'topup' in row[0].lower() :
                rctiErrorObj = RctiErrors()
                rctiErrorObj.clientName = clientName.clientId
                rctiErrorObj.docketNumber = None
                rctiErrorObj.docketDate = None
                rctiErrorObj.errorDescription = "topup"
                rctiErrorObj.fileName = fileName.split('@_!')[-1]
                rctiErrorObj.data = str(errorSolve)
                # rctiErrorObj.errorType = 1
                rctiErrorObj.save()
                
            elif  any(value in checkStr(row[0]) for value in manuallyManaged):
                for value in manuallyManaged:
                    if value in checkStr(row[0]):
                        rowErrorDescription = value
                        flag = True
                        strValue = row[0]

            elif flag and 'gst' in checkStr(row[0]):
                rctiErrorObj = RctiErrors()
                rctiErrorObj.clientName = clientName.clientId
                rctiErrorObj.docketNumber = None
                rctiErrorObj.docketDate = None
                rctiErrorObj.errorDescription = rowErrorDescription
                rctiErrorObj.fileName = fileName.split('@_!')[-1]
                rctiErrorObj.data = str(strValue) + str(errorSolve)
                # rctiErrorObj.errorType = 1
                rctiErrorObj.save()
                strValue = ''
                flag = False
            
            # docket number pattern like 'WI200941/1'  or 'T2' 
            elif re.fullmatch(datePattern, splitRow[0].strip()) and (len(splitRow[1].strip()) > 8 or len(str(splitRow[1].strip())) < 3):
                rctiErrorObj = RctiErrors()
                rctiErrorObj.clientName = clientName.clientId
                rctiErrorObj.docketNumber = None
                rctiErrorObj.docketDate = None
                rctiErrorObj.errorDescription = "Manually Manage."
                rctiErrorObj.fileName = fileName.split('@_!')[-1]
                rctiErrorObj.data = str(errorSolve)
                # rctiErrorObj.errorType = 1
                rctiErrorObj.save()

            elif len(splitRow) > 0:
                if re.fullmatch(datePattern, splitRow[0].strip()) and re.fullmatch(docketPattern, splitRow[1].strip()):
                    tempData.insert(0,splitRow[0])
                    tempData.insert(1,splitRow[1])
                    try:
                        if '-' in splitRow[2] and float(splitRow[2].replace('-','')):
                            rctiErrorObj = RctiErrors()
                            rctiErrorObj.clientName = clientName.clientId
                            rctiErrorObj.docketNumber = None
                            rctiErrorObj.docketDate = None
                            rctiErrorObj.errorDescription = "Manually Manage."
                            rctiErrorObj.fileName = fileName.split('@_!')[-1]
                            rctiErrorObj.data = str(errorSolve)
                            # rctiErrorObj.errorType = 1
                            
                            rctiErrorObj.save()
                            continue
                        else:
                            tempData.insert(2,str(float(splitRow[2].strip())))

                            tempData.insert(3,splitRow[3].strip())
                            tempData.insert(4,splitRow[4].strip())
                            tempData.insert(5,splitRow[5].strip())
                            tempData.insert(6,splitRow[6].strip())
                            tempData.insert(7,splitRow[7].strip().replace(',',''))
                            tempData.insert(6,' '.join(splitRow[8:]))
                        
                    except:
                        if '-' in splitRow[-1] and float(splitRow[-1].replace('-','')):
                            rctiErrorObj = RctiErrors()
                            rctiErrorObj.clientName = clientName.clientId
                            rctiErrorObj.docketNumber = None
                            rctiErrorObj.docketDate = None
                            rctiErrorObj.errorDescription = "Manually Manage."
                            rctiErrorObj.fileName = fileName.split('@_!')[-1]
                            rctiErrorObj.data = str(errorSolve)
                            # rctiErrorObj.errorType = 1
                            
                            rctiErrorObj.save()
                            continue
                        else:
                            tempData.insert(3,splitRow[-1])
                            tempData.insert(2,' '.join(splitRow[2:-1]))
                    

                    
                    if len(prepared) > 1 and len(tempData) > 1:
                        if prepared[0] == tempData[0] and prepared[1] == tempData[1]: 
                            prepared.extend(tempData[2:])
                        else:
                                 
                            finalList.append([truckNo] + prepared )
                            prepared = tempData
                    else:
                        prepared = tempData
                    tempData = []
                else:
                    with open('holcimUtils.txt', 'a') as f:
                        f.write('pattern not match' + str(row) + fileName.split('@_!')[-1] + '\n')
                    with open('holcimUtils.txt','a')as f:
                        f.write('pattern not match'+ str(row) + fileName.split('@_!')[-1] +'\n')
            else:
                with open('holcimUtils.txt','a')as f:
                    f.write('len is 0'+ str(row) + fileName.split('@_!')[-1] +'\n')
                          
        finalList.append([truckNo] + prepared)
    except Exception as e:
        with open('holcimUtils.txt','a')as f:
            f.write('convert Error' +str(e) + fileName.split('@_!')[-1]  +'\n')
            
            
    for data in finalList:
        rctiReportObj = RctiReport.objects.filter(pk = rctiReportId).first()
        try:
            docketDate = datetime.strptime(data[1], '%d.%m.%Y').date()
            if len(data) > 0:
                rctiObj = RCTI.objects.filter(truckNo = float(data[0]) ,docketNumber=int(data[2]),docketDate = docketDate).first()
                if not rctiObj:
                    rctiObj = RCTI()
                rctiObj.clientName = clientName
                rctiObj.truckNo =data[0]
                rctiObj.docketNumber = data[2]
                rctiObj.docketDate =  docketDate

                if len(data) > 5:
                    rctiObj.cubicMl = data[3]
                    rctiObj.paidQty = data[4]
                    rctiObj.unit = data[5]
                    rctiObj.noOfKm = data[6]
                    rctiObj.destination = data[7]
                    rctiObj.cubicMiAndKmsCost = data[9]
                    rctiObj.cartageTotal = data[9]
                    dataList = data[10:]
                else:
                    dataList = data[3:]
                    
                while dataList:
                    if 'standby' in dataList[0].lower():
                        rctiObj.standByPerHalfHourDuration = dataList[1]
                        rctiObj.standByTotal =dataList[1]
                    elif 'sat' in dataList[0].lower() or 'mon-fri' in dataList[0].lower():
                        rctiObj.surchargeCost = dataList[1]
                        rctiObj.surchargeTotal = dataList[1]
                    elif 'wait' in dataList[0].lower():
                        rctiObj.waitingTimeCost = dataList[1]
                        rctiObj.waitingTimeTotal = dataList[1]
                    elif 'blowback' in dataList[0].lower():
                        rctiObj.blowBackCost = dataList[1]
                        rctiObj.blowBackTotal = dataList[1]
                    # elif 'topup' in dataList[0].lower().replace(' ',''):
                    #     rctiErrorObj.clientName = clientName.clientId
                    #     rctiErrorObj.docketNumber = rctiObj.docketNumber
                    #     rctiErrorObj.docketDate = rctiObj.docketDate
                    #     rctiErrorObj.errorDescription = "Manage Top-up."
                    #     rctiErrorObj.fileName = fileName
                    #     rctiErrorObj.data = str(data)
                    #     rctiErrorObj.save()
                    elif 'trucktrf' in dataList[0].lower():
                        rctiObj.transferKMCost = dataList[1]
                        rctiObj.transferKMTotal = dataList[1]
                    elif 'return' in dataList[0].lower():
                        rctiObj.returnPerKmPerCubicMeterCost = dataList[1]
                        rctiObj.returnKmTotal = dataList[1]
                    elif 'callout' in dataList[0].lower():
                        rctiObj.callOutCost = dataList[1]
                        rctiObj.callOutTotal = dataList[1]
                    else:
                        rctiObj.otherDescription += dataList[0]
                        rctiObj.othersCost = dataList[1] + convertIntoFloat(dataList[1])
                        rctiObj.othersTotal = dataList[1] + convertIntoFloat(dataList[1])
                    dataList = dataList[2:]
                rctiObj.rctiReport = rctiReportObj
                rctiObj.save()
                
                rctiObjData = RCTI.objects.filter(docketNumber = rctiObj.docketNumber , docketDate = rctiObj.docketDate ).first()
                reconciliationDocketObj = ReconciliationReport.objects.filter(docketNumber = rctiObj.docketNumber , docketDate = rctiObj.docketDate ).first()
                rctiTotalCost =   rctiObjData.cartageTotal + rctiObjData.waitingTimeTotal + rctiObjData.transferKMTotal + rctiObjData.standByTotal + rctiObjData.surchargeTotal + rctiObjData.callOutTotal + rctiObjData.blowBackTotal + rctiObjData.othersTotal
                if not reconciliationDocketObj :
                    reconciliationDocketObj = ReconciliationReport()
        
                reconciliationDocketObj.docketNumber =  rctiObjData.docketNumber
                # reconciliationDocketObj.truckConnectionId = rctiObjData.truckNo if reconciliationDocketObj.truckId == 0  else reconciliationDocketObj.truckId
                reconciliationDocketObj.docketDate =  rctiObjData.docketDate
                reconciliationDocketObj.rctiLoadAndKmCost =  rctiObjData.cartageTotal
                reconciliationDocketObj.clientId =  clientName.clientId
                reconciliationDocketObj.rctiWaitingTimeCost = rctiObjData.waitingTimeTotal
                reconciliationDocketObj.rctiTransferKmCost = rctiObjData.transferKMTotal
                reconciliationDocketObj.rctiStandByCost =  rctiObjData.standByTotal
                reconciliationDocketObj.rctiSurchargeCost =  rctiObjData.surchargeTotal
                reconciliationDocketObj.rctiCallOut =  rctiObjData.callOutTotal
                reconciliationDocketObj.rctiBlowBack =  rctiObjData.blowBackTotal
                reconciliationDocketObj.rctiOtherCost =  rctiObjData.othersTotal
                reconciliationDocketObj.rctiTotalCost =  round(rctiTotalCost,2) 
                reconciliationDocketObj.fromRcti = True 
                
                reconciliationDocketObj.save()
                checkMissingComponents(reconciliationDocketObj)
                reconciliationTotalCheck(reconciliationDocketObj)
            else:
                with open('holcim.txt','a')as f:
                    f.write('skip'+ ', '.join(data) + fileName.split('@_!')[-1]  +'\n')
        except Exception as e:
            with open('holcim.txt','a')as f:
                f.write('error' +str(e) + ', '.join(data) +  fileName.split('@_!')[-1] +'\n')
            rctiErrorObj = RctiErrors()
            rctiErrorObj.clientName = clientName.clientId
            rctiErrorObj.docketNumber = None
            rctiErrorObj.docketDate = None
            rctiErrorObj.exceptionText = e
            rctiErrorObj.errorDescription = "Manually Manage."
            rctiErrorObj.fileName = fileName.split('@_!')[-1]
            rctiErrorObj.data = ', '.join(data)
            # rctiErrorObj.errorType = 1
            rctiErrorObj.save()

    


