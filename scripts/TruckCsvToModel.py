from GearBox_app.models import *
from django.contrib.auth.models import User , Group
import pandas as pd
from datetime import datetime

def dateFormatForTruck(data:str):
    date_object = datetime.strptime(data, '%d/%m/%Y')
    formatted_date = date_object.strftime('%Y-%m-%d')
    return formatted_date

def run():
    f = open("Truck_entry_file.txt", 'r')
    file_read = f.read().split(',')
    file_name = file_read[0]
    userName = file_read[1]
    userObj = User.objects.filter(username=userName).first()
    fileName = f'static/Account/TruckEntry/{file_name}'

    # fileName = 'static/Account/TruckEntry/20240219061254@_!Truck list.xlsx'

    data = pd.read_excel(fileName)
    custom_information_column_name = []
    build_date_index = data.columns.get_loc('Build Date')
    custom_information_column_name = data.columns[build_date_index + 1: build_date_index + 7].tolist()
    
    for index, row in data.iterrows():
        try:
            truckInformationObj = None
            adminTruckObj = None
            adminTruckObj = AdminTruck.objects.filter(adminTruckNumber = row['Fleet #']).first()
            if  not adminTruckObj :
                adminTruckObj = AdminTruck()
            
            truckInformationObj = adminTruckObj.truckInformation
            
            if not truckInformationObj:
                truckInformationObj = TruckInformation()
            
            truckInformationObj.fleet = row['Fleet #']
            
            # groupObj = TruckGroup.objects.filter(name=row['Groups']).first()
            # if not groupObj and str(row['Groups']) != 'nan':
            #     groupObj = TruckGroup()
            #     groupObj.name = row['Groups']
            #     groupObj.save()
            # truckInformationObj.group = None if not groupObj else groupObj.id
            # try:
            #     subGroupObj = TruckSubGroup.objects.filter(truckGroup = groupObj, name=row['SubGroups']).first()
            # except Exception as e:
            #     truckEntryErrorObj = TruckEntryError()
            #     truckEntryErrorObj.truckNo = row['Fleet #']
            #     truckEntryErrorObj.errorDescription = e
            #     truckEntryErrorObj.exceptionText = e
            #     truckEntryErrorObj.fileName = file_name
            #     truckEntryErrorObj.status = False
            #     truckEntryErrorObj.save()
            #     continue
            # if not subGroupObj and str(row['SubGroups']) != 'nan' and str(row['Groups']) != 'nan':
            #     subGroupObj = TruckSubGroup()
            #     subGroupObj.truckGroup = groupObj
            #     subGroupObj.name = row['SubGroups']
            #     subGroupObj.save()
            # truckInformationObj.subGroup = None if not subGroupObj else subGroupObj.id
            
            truckInformationObj.vehicleType = None if str(row['Type']) == 'nan' else str(row['Type'])
            truckInformationObj.serviceGroup = None if str(row['Service Group']) == 'nan' else str(row['Service Group'])

            truckInformationObj.informationMake = None if str(row['Make']) == 'nan' else str(row['Make'])
            truckInformationObj.informationModel = None if str(row['Model']) == 'nan' else str(row['Model'])
            truckInformationObj.informationConfiguration = None if str(row['Configuration']) == 'nan' else str(row['Configuration'])
            truckInformationObj.informationChassis = None if str(row['VIN / Chassis #']) == 'nan' else str(row['VIN / Chassis #'])
            truckInformationObj.informationBuildYear = None if str(row['Build Date']) == 'nan' else str(row['Build Date'])
            truckInformationObj.informationIcon = None if str(row['Icon']) == 'nan' else str(row['Icon'])
            # truckInformationObj.customFieldLabel1 = custom_information_column_name[0]
            # truckInformationObj.customFieldLabel2 = custom_information_column_name[1]
            # truckInformationObj.customFieldLabel3 = custom_information_column_name[2]
            # truckInformationObj.customFieldLabel4 = custom_information_column_name[3]
            # truckInformationObj.customFieldLabel5 = custom_information_column_name[4]
            # truckInformationObj.customFieldLabel6 = custom_information_column_name[5]
            # truckInformationObj.customFieldValue1 = None if str(row[custom_information_column_name[0]]) == 'nan' else str(row[custom_information_column_name[0]])
            # truckInformationObj.customFieldValue2 = None if str(row[custom_information_column_name[1]]) == 'nan' else str(row[custom_information_column_name[1]])
            # truckInformationObj.customFieldValue3 = None if str(row[custom_information_column_name[2]]) == 'nan' else str(row[custom_information_column_name[2]])
            # truckInformationObj.customFieldValue4 = None if str(row[custom_information_column_name[3]]) == 'nan' else str(row[custom_information_column_name[3]])
            # truckInformationObj.customFieldValue5 = None if str(row[custom_information_column_name[4]]) == 'nan' else str(row[custom_information_column_name[4]])
            # truckInformationObj.customFieldValue6 = None if str(row[custom_information_column_name[5]]) == 'nan' else str(row[custom_information_column_name[5]])
            truckInformationObj.customFieldLabel1 = 'Fuel Card'
            truckInformationObj.customFieldLabel2 = 'Old Fleet Number'
            truckInformationObj.customFieldLabel3 = 'Old Rego'
            truckInformationObj.customFieldLabel4 = 'Registered Owner'
            truckInformationObj.customFieldLabel5 = 'Roadside Assistance'
            truckInformationObj.customFieldLabel6 = 'PDD number'
            truckInformationObj.customFieldValue1 = None if str(row['Fuel Card']) == 'nan' else str(row['Fuel Card'])
            truckInformationObj.customFieldValue2 = None if str(row['Old Fleet Number']) == 'nan' else str(row['Old Fleet Number'])
            truckInformationObj.customFieldValue3 = None if str(row['Old Rego']) == 'nan' else str(row['Old Rego'])
            truckInformationObj.customFieldValue4 = None if str(row['Registered Owner']) == 'nan' else str(row['Registered Owner'])
            truckInformationObj.customFieldValue5 = None if str(row['Roadside Assistance']) == 'nan' else str(row['Roadside Assistance'])
            truckInformationObj.customFieldValue6 = None if str(row['PDD number']) == 'nan' else str(row['PDD number'])
            truckInformationObj.registered = True if str(row['Unregistered']) == 'false' else False
            truckInformationObj.registration = None if str(row['Registration']) == 'nan' else str(row['Registration']) 
            truckInformationObj.registrationCode = None if str(row['Code']) == 'nan' else str(row['Code']) 
            truckInformationObj.registrationState = None if str(row['State']) == 'nan' else str(row['State']) 
            truckInformationObj.registrationDueDate =  None if str(row['Registration Due']) == 'nan' else dateFormatForTruck(row['Registration Due'])
            truckInformationObj.registrationInterval = None if str(row['Interval']) == 'nan' else row['Interval']
            truckInformationObj.powered = True if str(row['Powered']) == 'true' else False
            truckInformationObj.engine = None if str(row['Engine No#']) == 'nan' else row['Engine No#']
            truckInformationObj.engineMake = None if str(row['Engine Make']) == 'nan' else row['Engine Make']
            truckInformationObj.engineModel = None if str(row['Engine Model']) == 'nan' else row['Engine Model']
            truckInformationObj.engineCapacity = None if str(row['Capacity']) == 'nan' else row['Capacity']
            truckInformationObj.engineGearBox = None if str(row['Gearbox']) == 'nan' else row['Gearbox']
            truckInformationObj.save()
            
            truckSettingObj = adminTruckObj.truckSetting
            if not truckSettingObj:
                truckSettingObj = TruckSetting()
            
            truckSettingObj.fuelType = row['Fuel Type']
            truckSettingObj.fuelCreditCategory = row['Fuel Credit Category']
            truckSettingObj.adbluePercent = row['Adblue %']
            truckSettingObj.kilometersOffset = row['Kilometres Offset']
            truckSettingObj.hoursOffset = row['Hours Offset']
            truckSettingObj.preStartChecklist = row['Check List']
            truckSettingObj.trailers = row['Linked Asset(s)']
            truckSettingObj.GCM = row['GCM']
            truckSettingObj.GVM = row['GVM']
            truckSettingObj.TARE = row['TARE']
            truckSettingObj.ATM = row['ATM']
            truckSettingObj.length = row['Length']
            truckSettingObj.height = row['Height']
            truckSettingObj.width = row['Width']
            truckSettingObj.volume = row['Volume']
            truckSettingObj.pallets = row['Pallets']
            truckSettingObj.customText1 = None
            truckSettingObj.customValue1 = row['Spare Field 7']
            truckSettingObj.customText2 = None
            truckSettingObj.customValue2 = row['Spare Field 8']
            truckSettingObj.customText3 = None
            truckSettingObj.customValue3 = row['Spare Field 9']
            truckSettingObj.customText4 = None
            truckSettingObj.customValue4 = row['Spare Field 10']
            truckSettingObj.customText5 = None
            truckSettingObj.customValue5 = row['Spare Field 11']
            truckSettingObj.customText6 = None
            truckSettingObj.customValue6 = row['Spare Field 12']
            truckSettingObj.customText7 = None
            truckSettingObj.customValue7 = row['Spare Field 13']
            truckSettingObj.customText8 = None
            truckSettingObj.customValue8 = row['Spare Field 14']
            truckSettingObj.customText9 = None
            truckSettingObj.customValue9 = row['Spare Field 15']
            truckSettingObj.customText10 = None
            truckSettingObj.customValue10 = row['Spare Field 16']
            truckSettingObj.customText11 = None
            truckSettingObj.customValue11 = row['Spare Field 17']
            truckSettingObj.customText12 = None
            truckSettingObj.customValue12 = row['Spare Field 18']
            truckSettingObj.customText13 = None
            truckSettingObj.customValue13 = row['Spare Field 19']
            truckSettingObj.customText14 = None
            truckSettingObj.customValue14 = row['Spare Field 20']
            truckSettingObj.customText15 = None
            truckSettingObj.customValue15 = row['Vehicle Notes']
            truckSettingObj.customText16 = None
            truckSettingObj.customValue16 = None
            truckSettingObj.save()
            
            adminTruckObj.adminTruckNumber = row['Fleet #']
            adminTruckObj.truckInformation = truckInformationObj
            adminTruckObj.truckSetting = truckSettingObj
            adminTruckObj.truckActive = True
            adminTruckObj.createdBy = userObj
            adminTruckObj.save()
        except Exception as e:
            # print(e)
            truckEntryErrorObj = TruckEntryError()
            truckEntryErrorObj.truckNo = row['Fleet #']
            truckEntryErrorObj.errorDescription = e
            truckEntryErrorObj.exceptionText = e
            truckEntryErrorObj.fileName = file_name
            truckEntryErrorObj.status = False
            truckEntryErrorObj.save()
            continue
