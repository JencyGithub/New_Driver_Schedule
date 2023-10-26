import pandas as pd
from Account_app.models import *
from GearBox_app.models import *
from CRUD import *

def insertIntoDatabase(data,key):
    existingTrip = None
    
    # Trip save
    try:
        existingTrip = DriverTrip.objects.filter(truckNo = data[1],shiftDate = data[0]).values().first()
        
        if existingTrip:
            tripObj = DriverTrip.objects.get(pk=existingTrip['id'])
        else:
            driverName = data[4].strip().replace(' ','').lower()
            try:
                # basePlant = BasePlant.objects.get(pk=1) 
                client = Client.objects.get(name = 'Boral')
            except:
                client = Client.objects.create(name = "Boral")
            driver = Driver.objects.get(name = driverName)
            shiftType = 'Day'
            shiftDate =  str(data[0]).split(' ')[0]
            
            tripObj = DriverTrip(
                verified = True,
                driverId = driver,
                clientName = client,
                shiftType = shiftType,
                truckNo = data[1],
                shiftDate = shiftDate
            )
            tripObj.save()

        # Docket save
        existingDockets = DriverDocket.objects.filter(tripId = tripObj.id).count()
        tripObj.numberOfLoads = existingDockets + 1
                
        if tripObj.startTime and tripObj.endTime:
            tripObj.startTime = getMaxTimeFromTwoTime(str(tripObj.startTime),str(data[6]),'min')
            tripObj.endTime = getMaxTimeFromTwoTime(str(tripObj.endTime),str(data[7]))
        else:
            tripObj.startTime = str(data[6])
            tripObj.endTime = str(data[7])
            
        tripObj.save()
        try:
            basePlant = BasePlant.objects.get(pk=1) 
        except:
            basePlant = BasePlant.objects.create(basePlant = "Not selected")
            
        
        docketObj = DriverDocket(
            shiftDate = ' ' if str(data[0]) == 'nan' else data[0],
            tripId = tripObj,
            docketNumber = data[5],
            noOfKm = 0 if str(data[10]) == 'nan' else data[10],
            transferKM = 0 if str(data[18]) == 'nan' else data[18],
            returnToYard = True if data[16] == 'Yes' else False,
            returnQty = 0 if str(data[14]) == 'nan' else data[14],
            returnKm = 0 if str(data[15]) == 'nan' else data[15],
            waitingTimeStart = 0 if str(data[11]) == 'nan' else data[11],
            waitingTimeEnd = 0 if str(data[12]) == 'nan' else data[12],
            totalWaitingInMinute = 0 if str(data[13]) == 'nan' else data[13],
            cubicMl = 0 if str(data[8]) == 'nan' else data[8],
            standByStartTime = ' ' if str(data[20]) == 'nan' else data[20],
            standByEndTime = ' ' if str(data[21]) == 'nan' else data[21],
            comment = data[17],
            basePlant = basePlant,
            # surcharge_type = ,
            # surcharge_duration = ,
            # others = ,
        )
        docketObj.save()
        
    except Exception as e:
        # print(f"Error : {e}, Row: {key}")    
        # print(f"Error : {data}")  
        txtFile = open('static/subprocessFiles/errorFromPastTrip.txt','a')
        txtFile.write(f'Line no : {key}, Error : {e} \n {data} \n\n\n')
        txtFile.close()

    return True

f = open("pastTrip_entry.txt", 'r')
file_name = f.read()

fileName = f'static/Account/PastTripsEntry/{file_name}'

txtFile = open('static/subprocessFiles/errorFromPastTrip.txt','w')
txtFile.write(f'File:{file_name}\n\n')
txtFile.close()

pastData = pd.read_excel(fileName)


for key,row in pastData.iterrows():
    try:
        insertIntoDatabase(row,key)
    except Exception as e:
        print(f" ! Error : {e}")

# trucks = [653, 654, 783, 784, 785, 786, 787, 782, 789, 550, 551, 552, 553, 554, 700, 701, 702, 703, 707, 708, 709, 719, 722, 723, 725, 726, 727, 728, 473, 470, 730, 471, 472, 731, 474, 475, 477]

# for truck in trucks:
#     try:
        
#         obj = AdminTruck(adminTruckNumber = truck)
#         obj.save()
#     except Exception as e:
#         print(f"Error : {e}")
        