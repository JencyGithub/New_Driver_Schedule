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
            
            if str(row['Groups']) != 'nan':
                groupObj = TruckGroup.objects.filter(name=row['Groups']).first()
                # if not groupObj:
                #     groupObj = TruckGroup()
                #     groupObj.name = row['Groups']
                #     groupObj.save()
                if groupObj:
                    truckInformationObj.group =  groupObj.id
                else:
                    truckEntryErrorObj = TruckEntryError()
                    truckEntryErrorObj.truckNo = row['Fleet #']
                    truckEntryErrorObj.errorDescription = 'Group  is none'
                    truckEntryErrorObj.exceptionText = e
                    truckEntryErrorObj.fileName = file_name
                    truckEntryErrorObj.status = False
                    truckEntryErrorObj.save()
                    continue
                
            else:
                truckEntryErrorObj = TruckEntryError()
                truckEntryErrorObj.truckNo = row['Fleet #']
                truckEntryErrorObj.errorDescription = 'Group  is not exist'
                truckEntryErrorObj.exceptionText = e
                truckEntryErrorObj.fileName = file_name
                truckEntryErrorObj.status = False
                truckEntryErrorObj.save()
                continue
            if str(row['SubGroups']) != 'nan':
                subGroupObj = TruckSubGroup.objects.filter(truckGroup = groupObj, name=row['SubGroups']).first()
                # if not subGroupObj:
                    #     subGroupObj = TruckSubGroup()
                    #     subGroupObj.truckGroup = groupObj
                    #     subGroupObj.name = row['SubGroups']
                    #     subGroupObj.save()
                if subGroupObj:
                    truckInformationObj.subGroup =  subGroupObj.id
                    
                else:
                    truckEntryErrorObj = TruckEntryError()
                    truckEntryErrorObj.truckNo = row['Fleet #']
                    truckEntryErrorObj.errorDescription = 'SubGroup is not exist.'
                    truckEntryErrorObj.exceptionText = 'SubGroup is not exist.'
                    truckEntryErrorObj.fileName = file_name
                    truckEntryErrorObj.status = False
                    truckEntryErrorObj.save()
                    continue
            else:
                truckEntryErrorObj = TruckEntryError()
                truckEntryErrorObj.truckNo = row['Fleet #']
                truckEntryErrorObj.errorDescription = 'SubGroup  is none'
                truckEntryErrorObj.exceptionText = 'SubGroup is not exist.'
                truckEntryErrorObj.fileName = file_name
                truckEntryErrorObj.status = False
                truckEntryErrorObj.save()
                continue
            
            
            
            
            truckInformationObj.vehicleType = '' if str(row['Type']) == 'nan' else str(row['Type'])
            truckInformationObj.serviceGroup = '' if str(row['Service Group']) == 'nan' else str(row['Service Group'])

            truckInformationObj.informationMake = '' if str(row['Make']) == 'nan' else str(row['Make'])
            truckInformationObj.informationModel = '' if str(row['Model']) == 'nan' else str(row['Model'])
            truckInformationObj.informationConfiguration = '' if str(row['Configuration']) == 'nan' else str(row['Configuration'])
            truckInformationObj.informationChassis = '' if str(row['VIN / Chassis #']) == 'nan' else str(row['VIN / Chassis #'])
            truckInformationObj.informationBuildYear = '' if str(row['Build Date']) == 'nan' else str(row['Build Date'])
            truckInformationObj.informationIcon = '' if str(row['Icon']) == 'nan' else str(row['Icon'])
            truckInformationObj.customFieldLabel1 = custom_information_column_name[0]
            truckInformationObj.customFieldLabel2 = custom_information_column_name[1]
            truckInformationObj.customFieldLabel3 = custom_information_column_name[2]
            truckInformationObj.customFieldLabel4 = custom_information_column_name[3]
            truckInformationObj.customFieldLabel5 = custom_information_column_name[4]
            truckInformationObj.customFieldLabel6 = custom_information_column_name[5]
            truckInformationObj.customFieldValue1 = '' if str(row[custom_information_column_name[0]]) == 'nan' else str(row[custom_information_column_name[0]])
            truckInformationObj.customFieldValue2 = '' if str(row[custom_information_column_name[1]]) == 'nan' else str(row[custom_information_column_name[1]])
            truckInformationObj.customFieldValue3 = '' if str(row[custom_information_column_name[2]]) == 'nan' else str(row[custom_information_column_name[2]])
            truckInformationObj.customFieldValue4 = '' if str(row[custom_information_column_name[3]]) == 'nan' else str(row[custom_information_column_name[3]])
            truckInformationObj.customFieldValue5 = '' if str(row[custom_information_column_name[4]]) == 'nan' else str(row[custom_information_column_name[4]])
            truckInformationObj.customFieldValue6 = '' if str(row[custom_information_column_name[5]]) == 'nan' else str(row[custom_information_column_name[5]])
            # truckInformationObj.customFieldLabel1 = 'Fuel Card'
            # truckInformationObj.customFieldLabel2 = 'Old Fleet Number'
            # truckInformationObj.customFieldLabel3 = 'Old Rego'
            # truckInformationObj.customFieldLabel4 = 'Registered Owner'
            # truckInformationObj.customFieldLabel5 = 'Roadside Assistance'
            # truckInformationObj.customFieldLabel6 = 'PDD number'
            # truckInformationObj.customFieldValue1 = '' if str(row['Fuel Card']) == 'nan' else str(row['Fuel Card'])
            # truckInformationObj.customFieldValue2 = '' if str(row['Old Fleet Number']) == 'nan' else str(row['Old Fleet Number'])
            # truckInformationObj.customFieldValue3 = '' if str(row['Old Rego']) == 'nan' else str(row['Old Rego'])
            # truckInformationObj.customFieldValue4 = '' if str(row['Registered Owner']) == 'nan' else str(row['Registered Owner'])
            # truckInformationObj.customFieldValue5 = '' if str(row['Roadside Assistance']) == 'nan' else str(row['Roadside Assistance'])
            # truckInformationObj.customFieldValue6 = '' if str(row['PDD number']) == 'nan' else str(row['PDD number'])
            truckInformationObj.registered = True if str(row['Unregistered']) == 'false' else False
            truckInformationObj.registration = '' if str(row['Registration']) == 'nan' else str(row['Registration']) 
            truckInformationObj.registrationCode = '' if str(row['Code']) == 'nan' else str(row['Code']) 
            truckInformationObj.registrationState = '' if str(row['State']) == 'nan' else str(row['State']) 
            truckInformationObj.registrationDueDate =  '' if str(row['Registration Due']) == 'nan' else dateFormatForTruck(row['Registration Due'])
            truckInformationObj.registrationInterval = '' if str(row['Interval']) == 'nan' else row['Interval']
            truckInformationObj.powered = True if str(row['Powered']) == 'true' else False
            truckInformationObj.engine = '' if str(row['Engine No#']) == 'nan' else row['Engine No#']
            truckInformationObj.engineMake = '' if str(row['Engine Make']) == 'nan' else row['Engine Make']
            truckInformationObj.engineModel = '' if str(row['Engine Model']) == 'nan' else row['Engine Model']
            truckInformationObj.engineCapacity = '' if str(row['Capacity']) == 'nan' else row['Capacity']
            truckInformationObj.engineGearBox = '' if str(row['Gearbox']) == 'nan' else row['Gearbox']
            truckInformationObj.save()
            
            truckSettingObj = adminTruckObj.truckSetting
            if not truckSettingObj:
                truckSettingObj = TruckSetting()
            
            truckSettingObj.fuelType = '' if str(row['Fuel Type']) == 'nan' else row['Fuel Type']
            truckSettingObj.fuelCreditCategory = '' if str(row['Fuel Credit Category']) == 'nan' else row['Fuel Credit Category']
            truckSettingObj.adbluePercent = '' if str(row['Adblue %']) == 'nan' else row['Adblue %']
            truckSettingObj.kilometersOffset = '' if str(row['Kilometres Offset']) == 'nan' else row['Kilometres Offset']
            truckSettingObj.hoursOffset = '' if str(row['Hours Offset']) == 'nan' else row['Hours Offset']
            truckSettingObj.preStartChecklist = '' if str(row['Check List']) == 'nan' else row['Check List']
            truckSettingObj.trailers = '' if str(row['Linked Asset(s)']) == 'nan' else row['Linked Asset(s)']
            truckSettingObj.GCM = '' if str(row['GCM']) == 'nan' else row['GCM']
            truckSettingObj.GVM = '' if str(row['GVM']) == 'nan' else row['GVM']
            truckSettingObj.TARE = '' if str(row['TARE']) == 'nan' else row['TARE']
            truckSettingObj.ATM = '' if str(row['ATM']) == 'nan' else row['ATM']
            truckSettingObj.length = '' if str(row['Length']) == 'nan' else row['Length']
            truckSettingObj.height = '' if str(row['Height']) == 'nan' else row['Height']
            truckSettingObj.width = '' if str(row['Width']) == 'nan' else row['Width']
            truckSettingObj.volume = '' if str(row['Volume']) == 'nan' else row['Volume']
            truckSettingObj.pallets = '' if str(row['Pallets']) == 'nan' else row['Pallets']
            truckSettingObj.customText1 = None
            truckSettingObj.customValue1 = '' if str(row['Spare Field 7']) == 'nan' else row['Spare Field 7']
            truckSettingObj.customText2 = None
            truckSettingObj.customValue2 = '' if str(row['Spare Field 8']) == 'nan' else row['Spare Field 8']
            truckSettingObj.customText3 = None
            truckSettingObj.customValue3 = '' if str(row['Spare Field 9']) == 'nan' else row['Spare Field 9']
            truckSettingObj.customText4 = None
            truckSettingObj.customValue4 = '' if str(row['Spare Field 10']) == 'nan' else row['Spare Field 10']
            truckSettingObj.customText5 = None
            truckSettingObj.customValue5 = '' if str(row['Spare Field 11']) == 'nan' else row['Spare Field 11']
            truckSettingObj.customText6 = None
            truckSettingObj.customValue6 = '' if str(row['Spare Field 12']) == 'nan' else row['Spare Field 12']
            truckSettingObj.customText7 = None
            truckSettingObj.customValue7 = '' if str(row['Spare Field 13']) == 'nan' else row['Spare Field 13']
            truckSettingObj.customText8 = None
            truckSettingObj.customValue8 = '' if str(row['Spare Field 14']) == 'nan' else row['Spare Field 14']
            truckSettingObj.customText9 = None
            truckSettingObj.customValue9 = '' if str(row['Spare Field 15']) == 'nan' else row['Spare Field 15']
            truckSettingObj.customText10 = None
            truckSettingObj.customValue10 = '' if str(row['Spare Field 16']) == 'nan' else row['Spare Field 16']
            truckSettingObj.customText11 = None
            truckSettingObj.customValue11 = '' if str(row['Spare Field 17']) == 'nan' else row['Spare Field 17']
            truckSettingObj.customText12 = None
            truckSettingObj.customValue12 = '' if str(row['Spare Field 18']) == 'nan' else row['Spare Field 18']
            truckSettingObj.customText13 = None
            truckSettingObj.customValue13 = '' if str(row['Spare Field 19']) == 'nan' else row['Spare Field 19']
            truckSettingObj.customText14 = None
            truckSettingObj.customValue14 = '' if str(row['Spare Field 20']) == 'nan' else row['Spare Field 20']
            truckSettingObj.customText15 = None
            truckSettingObj.customValue15 = '' if str(row['Vehicle Notes']) == 'nan' else row['Vehicle Notes']
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
