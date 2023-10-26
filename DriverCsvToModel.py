import csv, re
from GearBox_app.models import *
from django.contrib.auth.models import User , Group
import pandas as pd

def get_valid_mobile_number(mobile_no): 
    if len(str(mobile_no)) == 10:
        return mobile_no  
    else:
        return None
            
def insertIntoModel(dataList):
    dump = dataList[:5]  
    M_pattern = get_valid_mobile_number(dump[2])
    users = User.objects.all()

    usernames = [user.username for user in users]
    email_addresses = [user.email for user in users]
    if dump[2] == M_pattern and dump[1].strip().replace(' ','') not in usernames and dump[3].strip().replace(' ','') not in email_addresses:
        DriverObj = Driver()
        DriverObj.driverId = dump[0]
        DriverObj.name = dump[1].strip().replace(' ','').lower()
        DriverObj.phone = dump[2] 
        DriverObj.email = dump[3].strip().replace(' ','')
        DriverObj.password = dump[4].strip()
        
        user_ = User.objects.create(
            username=DriverObj.name,
            email=DriverObj.email,
            password=DriverObj.password,
            is_staff=True,
        )  
        group = Group.objects.get(name='Driver')
        user_.groups.add(group)
        
        user_.set_password(DriverObj.password)
        user_.save()
        DriverObj.save()
        

f = open("Driver_reg_file.txt", 'r')
file_name = f.read()

fileName = f'static/Account/DriverEntry/{file_name}'

df = pd.read_excel(fileName)
for index, row in df.iterrows():
    insertIntoModel(row)