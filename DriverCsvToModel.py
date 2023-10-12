import csv, re
from GearBox_app.models import *
from django.contrib.auth.models import User , Group

def get_valid_mobile_number(mobile_no):       
    if re.fullmatch('[0-9]{10}', mobile_no):
        return mobile_no
    else:
        return None
            
def insertIntoModel(dataList):
    dump = dataList[:4]
    mobile_no = dump[1].strip()
    M_pattern = get_valid_mobile_number(mobile_no)
    users = User.objects.all()

    usernames = [user.username for user in users]
    email_addresses = [user.email for user in users]
    if dump[1].strip() == M_pattern and dump[0].strip().replace(' ','') not in usernames and dump[2].strip().replace(' ','') not in email_addresses:
        DriverObj = Driver()
        DriverObj.name = dump[0].strip().replace(' ','')
        DriverObj.phone = dump[1].strip() 
        DriverObj.email = dump[2].strip().replace(' ','')
        DriverObj.password = dump[3].strip()
        
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

        
f = open("File_name_file.txt", 'r')
file_name = f.read()
with open('File_name_file.txt', 'w') as f:
    f.write('')

files = open(f'static/Account/DriverEntry/{file_name}','r')
reader=csv.reader(files)


next(reader)
for row in reader:
    insertIntoModel(row)