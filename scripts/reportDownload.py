import json, csv
from Account_app.models import *
from GearBox_app.models import *
from Appointment_app.models import *

def setDataList(givenRecObjs, reportType):
    try:
        for recObj in givenRecObjs:
            recObj['reconciliationType'] = reportType
            clientTruckConnectionObj = ClientTruckConnection.objects.filter(pk=recObj['truckConnectionId']).first()
            if clientTruckConnectionObj:
                rctiObj = RCTI.objects.filter(docketNumber=recObj['docketNumber'], docketDate=recObj['docketDate'], clientName__clientId=recObj['clientId'], truckNo=clientTruckConnectionObj.clientTruckId).first()
                driverDocketObj = DriverShiftDocket.objects.filter(docketNumber=recObj['docketNumber'], shiftDate=recObj['docketDate'], clientId=recObj['clientId'] , truckConnectionId=clientTruckConnectionObj.id).first()

            recObj['clientId'] = rctiObj.clientName.name if rctiObj else ''
            recObj['truckConnectionId'] = rctiObj.truckNo if rctiObj else ''
            
            recObj['fileName'] = rctiObj.rctiReport.fileName if rctiObj else ''
            recObj['depot'] = rctiObj.docketYard if rctiObj else ''
            
            # RCTI data
            recObj['rctiNoOfKm'] = rctiObj.noOfKm if rctiObj else ''
            recObj['rctiCubicMl'] = rctiObj.cubicMl if rctiObj else ''
            recObj['rctiDestination'] = rctiObj.destination if rctiObj else ''
            recObj['rctiUnit'] = rctiObj.unit if rctiObj else ''
            recObj['rctiPaidQty'] = rctiObj.paidQty if rctiObj else ''
            recObj['rctiTransferKM'] = rctiObj.transferKM if rctiObj else ''
            recObj['rctiReturnKm'] = rctiObj.returnKm if rctiObj else ''
            recObj['rctiWaitingTimeInMinutes'] = rctiObj.waitingTimeInMinutes if rctiObj else ''
            recObj['rctiStandByNoSlot'] = rctiObj.standByNoSlot if rctiObj else ''
            recObj['rctiMinimumLoad'] = rctiObj.minimumLoad if rctiObj else ''
            recObj['rctiBlowBack'] = rctiObj.blowBack if rctiObj else ''
            recObj['rctiCallOut'] = rctiObj.callOut if rctiObj else ''
            recObj['rctiSurcharge'] = rctiObj.surcharge if rctiObj else ''
            recObj['rctiOthers'] = rctiObj.others if rctiObj else ''
            recObj['rctiOtherDescription'] = rctiObj.otherDescription if rctiObj else ''
            
            # Driver Docket data
            recObj['driverNoOfKm'] = driverDocketObj.noOfKm if driverDocketObj else ''
            recObj['driverTransferKM'] = driverDocketObj.transferKM if driverDocketObj else ''
            recObj['driverReturnQty'] = driverDocketObj.returnQty if driverDocketObj else ''
            recObj['driverReturnKm'] = driverDocketObj.returnKm if driverDocketObj else ''
            recObj['driverWaitingTimeStart'] = driverDocketObj.waitingTimeStart if driverDocketObj else ''
            recObj['driverWaitingTimeEnd'] = driverDocketObj.waitingTimeEnd if driverDocketObj else ''
            recObj['driverCubicMl'] = driverDocketObj.cubicMl if driverDocketObj else ''
            recObj['driverStandByStartTime'] = driverDocketObj.standByStartTime if driverDocketObj else ''
            recObj['driverStandByEndTime'] = driverDocketObj.standByEndTime if driverDocketObj else ''
            recObj['driverBlowBack'] = driverDocketObj.blowBack if driverDocketObj else ''
            recObj['driverCallOut'] = driverDocketObj.callOut if driverDocketObj else ''
            recObj['driverMinimumLoad'] = driverDocketObj.minimumLoad if driverDocketObj else ''
            recObj['driverOthers'] = driverDocketObj.others if driverDocketObj else ''
            recObj['driverComment'] = driverDocketObj.comment if driverDocketObj else ''
            recObj['driverReturnToYard'] = driverDocketObj.returnToYard if driverDocketObj else ''
            recObj['driverTippingToYard'] = driverDocketObj.tippingToYard if driverDocketObj else ''

            recObj.pop('id')
            recObj.pop('fromDriver')
            recObj.pop('fromRcti')
            
        # return givenRecObjs
        return setCsvData(givenRecObjs)
        
    except Exception as e:
        pass
    
def setCsvData(dataDict):
    try:
        header = list(dataDict[0].keys())
        appendList = []
        for obj in dataDict:
            appendList.append(list(obj.values()))
        appendList.insert(0, header)
        return appendList
    except Exception as e:
        # print(e)
        pass
    
def saveFile(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
try: 
    with open('scripts/data.json', 'r') as file:
        data = json.load(file)
        
    startDate, endDate, dataType, reportType = data['reportDownload']['startDate'], data['reportDownload']['endDate'], data['reportDownload']['type'], data['reportDownload']['reportType']
    if startDate and endDate:
        csv_file = f"static/Account/ReportFiles/{reportType}_{startDate} to {endDate}_{data['reportDownload']['type'] }.csv"
        reconciliationObjs = ReconciliationReport.objects.filter(docketDate__range=(startDate, endDate),reconciliationType = dataType).values()

        appendData = setDataList(reconciliationObjs, reportType)
        saveFile(csv_file, appendData)
    
except Exception as e:
    # print(e)
    pass
            