import pandas as pd
from Account_app.models import *
from GearBox_app.models import *

def insertIntoDatabase(data):
    newTrip = None
    print(row)
    exit()
    
    return True

pastData = pd.read_excel('pastTrip.xlsx')

for key,row in pastData.iterrows():
    try:
        insertIntoDatabase(row)
    except Exception as e:
        print(f"Error : {e}")

# trucks = [653, 654, 783, 784, 785, 786, 787, 782, 789, 550, 551, 552, 553, 554, 700, 701, 702, 703, 707, 708, 709, 719, 722, 723, 725, 726, 727, 728, 473, 470, 730, 471, 472, 731, 474, 475, 477]

# for truck in trucks:
#     try:
        
#         obj = AdminTruck(adminTruckNumber = truck)
#         obj.save()
#     except Exception as e:
#         print(f"Error : {e}")
        