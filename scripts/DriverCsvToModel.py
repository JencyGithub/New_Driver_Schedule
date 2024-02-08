from GearBox_app.models import *
from django.contrib.auth.models import User , Group


def run():
    f = open("Driver_reg_file.txt", 'r')
    file_name = f.read()


    fileName = f'static/Account/DriverEntry/{file_name}'

    # fileName = 'static/Account/DriverEntry/20231207043947@_!sampleDriverEntry.csv'

    # df = pd.read_excel(fileName)
    with open(fileName,'r') as f:
        count_ = 0
            
        for row in f:
            count_ += 1
            if count_ == 1:
                continue
            
            data = row.strip().split(',')
            # with open("Expense_error.txt", 'a')as f:
            #     f.write(str(data)+'\n')
            dump = data[:5]  
            if len(str(dump[2])) == 10:
                M_pattern =  dump[2]  
            else:
                M_pattern =  dump[2]  

            users = User.objects.all()

            usernames = [user.username for user in users]
            email_addresses = [user.email for user in users]
            # print(usernames,email_addresses)
            try:
                driverName = dump[1].lower().strip().replace(' ','').replace('-','').replace('(','').replace(')','')
                if  driverName not in usernames and dump[3].strip().replace(' ','') not in email_addresses:
                    DriverObj = Driver()
                    DriverObj.driverId = dump[0]
                    DriverObj.name = driverName.lower()
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
                else:
                    
                    with open("Driver_skip.txt", 'a')as f:
                        f.write(str(dump)+ str(file_name) + '\n')
            except Exception as e:
                with open("Driver_entry_error.txt", 'a')as f:
                    f.write(str(e)+str(data)+'\n')
            

