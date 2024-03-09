from Account_app.models import *
import datetime 
from django.core.mail import send_mail
import time


def run():
    
    with open('C:/Users/Administrator/Desktop/New_Driver_Schedule/New_Driver_Schedule/scripts/sendEmailOnPreStartAndShiftEndNotFilled.txt','r')as f:
        data = f.read().strip()
        if  data != '':
            sendEmailOnPreStartAndShiftEndNotFilled_last_UTC_runtime = datetime.datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
        else:
            sendEmailOnPreStartAndShiftEndNotFilled_last_UTC_runtime = None
    currentUTC = datetime.datetime.utcnow()
    preStartNotFilledQuerySet = DriverShift.objects.filter(endTimeUTC = None , startTimeUTC__lte = currentUTC-datetime.timedelta(minutes=15)) #get all the shifts that have not ended yet
    for obj in preStartNotFilledQuerySet:
        tripObj = DriverShiftTrip.objects.filter(shiftId=obj.id , startTimeUTC = None).first()
        if  tripObj or not DriverShiftTrip.objects.filter(shiftId = obj.id).first() :
            driverObj = Driver.objects.filter(driverId = obj.driverId).first()
            driverMessage = f'Driver Name : {driverObj.firstName} {driverObj.middleName} {driverObj.lastName}'
            subject = f'Critical : Pre-start Not Filed for  {driverObj.firstName} {driverObj.middleName} {driverObj.lastName}'
            bodyMessage = 'Hi Agi Hire,\n\nFollowing driver has not filled the pre-start for truck'
            locationMessage = f'Location : Latitude - {obj.latitude} , Longitude = {obj.longitude} '
            startTime = f'Start Time : {obj.startDateTime}'
            
            
            message = f'{bodyMessage}\n{driverMessage}\n{locationMessage}\n{startTime}'
            from_email = 'siddhantethansrec@gmail.com'  # Replace with your email
            mailSendList = [ 'agihire@pnrgroup.com.au']
            # agihire@pnrgroup.com.au
            send_mail(subject, message, from_email, recipient_list=mailSendList)
    
    activeShiftQuerySet = DriverShift.objects.filter(endTimeUTC = None , endDateTime = None)
    for obj in activeShiftQuerySet:
        if obj.startTimeUTC is not None and (currentUTC-obj.startTimeUTC).total_seconds()> 12*60*60 :
            if sendEmailOnPreStartAndShiftEndNotFilled_last_UTC_runtime is None or sendEmailOnPreStartAndShiftEndNotFilled_last_UTC_runtime.hour < currentUTC.hour:
                driverObj = Driver.objects.filter(driverId = obj.driverId).first()
                subject = f'Warning : Shift not ended by {driverObj.firstName} {driverObj.middleName} {driverObj.lastName}'
                bodyMessage = 'Hi Agi Hire,\n\nFollowing driver has not ended the shift for truck'
                driverMessage = f'Driver Name : {driverObj.firstName} {driverObj.middleName} {driverObj.lastName}'
                locationMessage = f'Location : Latitude - {obj.latitude} , Longitude = {obj.longitude} '
                startTime = f'Start Time : {obj.startDateTime}'
                
                
                message = f'{bodyMessage}\n{driverMessage}\n{locationMessage}\n{startTime}'
                from_email = 'siddhantethansrec@gmail.com'  # Replace with your email
                mailSendList = ['agihire@pnrgroup.com.au']
                # agihire@pnrgroup.com.au
                time.sleep(1)
                send_mail(subject, message, from_email, recipient_list=mailSendList)
    sendEmailOnPreStartAndShiftEndNotFilled_last_UTC_runtime = currentUTC
    
    with open('C:/Users/Administrator/Desktop/New_Driver_Schedule/New_Driver_Schedule/scripts/sendEmailOnPreStartAndShiftEndNotFilled.txt','w')as f:
        f.write(currentUTC.strftime('%Y-%m-%d %H:%M:%S'))