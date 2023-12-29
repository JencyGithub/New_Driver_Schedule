import re,csv
from Account_app.models import *
from GearBox_app.models import *
from Appointment_app.models import *
from datetime import datetime

with open('File_name_file.txt','r')as f:
    fileName = f.read()
    
with open(f'static/Account/RCTI/RCTIInvoice/{fileName}','r') as f:
    rctiErrorObj = RctiErrors()
    csv_reader = csv.reader(f)
    clientName = Client.objects.filter(name = 'holcim').first()
    finalList = []
    prepared = []
    tempData = []
    lineCount = 0
    datePattern = r'\d{2}\.\d{2}\.\d{4}'
    docketPattern = r'(\d{8}[a-zA-Z]{0,2})'
    try:
        for row in csv_reader:
            lineCount += 1
            if lineCount == 3117:
                print()
            if '@' in row[0]:
                row[0]=row[0].replace(' @ ','@')
            splitRow = row[0].split()
            splitRow = list(filter(lambda x: x.strip() != '', splitRow))
            if len(splitRow) > 0:
                if re.fullmatch(datePattern, splitRow[0].strip()) and re.fullmatch(docketPattern, splitRow[1].strip()):
                    tempData.insert(0,splitRow[0])
                    tempData.insert(1,splitRow[1])
                    try:
                        tempData.insert(2,str(float(splitRow[2].strip())))
                        tempData.insert(3,splitRow[3].strip())
                        tempData.insert(4,splitRow[4].strip())
                        tempData.insert(5,splitRow[5].strip())
                        tempData.insert(6,splitRow[6].strip())
                        tempData.insert(7,splitRow[7].strip())
                        tempData.insert(6,' '.join(splitRow[8:]))
                        
                    except:
                        tempData.insert(3,splitRow[-1])
                        tempData.insert(2,' '.join(splitRow[2:-1]))
                        
                    if len(prepared) > 1 and len(tempData) > 1:
                        if prepared[0] == tempData[0] and prepared[1] == tempData[1]: 
                            prepared.extend(tempData[2:])
                        else:
                            finalList.append(prepared)
                            

                            prepared = tempData
                    else:
                        prepared = tempData
                    tempData = []
                        
        finalList.append(prepared)
        for data in finalList:
            try:
                if len(data) > 5:
                    rctiObj = RCTI()
                    rctiObj.clientName = clientName
                    rctiObj.docketNumber = data[1]
                    rctiObj.docketDate =  datetime.strptime(data[0], '%d.%m.%Y').date()

                    
                    rctiObj.cubicMl = data[2]
                    rctiObj.paidQty = data[3]
                    rctiObj.unit = data[4]
                    rctiObj.noOfKm = data[5]
                    rctiObj.destination = data[6]
                    rctiObj.cubicMiAndKmsCost = data[8]
                    rctiObj.cartageTotal = data[8]
                    dataList = data[9:]
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
                        elif 'topup' in dataList[0].lower().replace(' ',''):
                            rctiErrorObj.clientName = 'boral'
                            rctiErrorObj.docketNumber = rctiObj.docketNumber
                            rctiErrorObj.docketDate = rctiObj.docketDate
                            rctiErrorObj.errorDescription = "Manage Top-up."
                            rctiErrorObj.fileName = fileName
                            rctiErrorObj.data = str(data)
                            rctiErrorObj.save()
                            
                        elif 'trucktrf' in dataList[0].lower():
                            rctiObj.transferKMCost = dataList[1]
                            rctiObj.transferKMTotal = dataList[1]
                        elif 'return' in dataList[0].lower():
                            rctiObj.returnPerKmPerCubicMeterCost = dataList[1]
                            rctiObj.returnKmTotal = dataList[1]
                        elif 'callout' in dataList[0].lower():
                            rctiObj.callOutCost = dataList[1]
                            rctiObj.callOutTotal = dataList[1]
                        dataList = dataList[2:]
                    
                    rctiObj.save()
                else:
                    print(f'data:{data}') 
            except Exception as e:
                print(f'Inside Error:{e}')
    except Exception as e:
        print(f'Error:{e}')
        
        


