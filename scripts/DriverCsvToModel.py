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
            dump = data[:7]

            if len(str(dump[1])) == 10:
                M_pattern =  dump[1]  
            elif len(str(dump[1])) == 9:
                M_pattern = '0' + dump[1]
            else:
                M_pattern = '' 

            users = User.objects.all()

            usernames = [user.username for user in users]
            email_addresses = [user.email for user in users]
            # print(usernames,email_addresses)
            try:
                driverName = dump[0].lower().strip().replace(' ','').replace('-','').replace('(','').replace(')','')
                if driverName not in usernames and dump[2].strip().replace(' ','') not in email_addresses:
                    DriverObj = Driver()
                    # DriverObj.driverId = dump[0]
                    DriverObj.name = driverName.lower()
                    DriverObj.phone = dump[1] 
                    DriverObj.email = dump[2].strip().replace(' ','')
                    DriverObj.password = dump[3].strip()

                    DriverObj.firstName = dump[4].strip()
                    DriverObj.middleName = dump[5].strip() if dump[5].strip() else ''
                    DriverObj.lastName = dump[6].strip()

                    user_ = User.objects.create(
                        username=DriverObj.name,
                        email=DriverObj.email,
                        password=DriverObj.password,
                        first_name = DriverObj.firstName,
                        last_name = DriverObj.lastName,
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
                # print(e)
                with open("Driver_entry_error.txt", 'a')as f:
                    f.write(str(e)+str(data)+'\n')
            

