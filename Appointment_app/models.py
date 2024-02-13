from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from GearBox_app.models import *
from Account_app.models import *

class Appointment(models.Model):
    TRIP_STATUS = [
        ('Unassigned', 'Unassigned'),
        ('Assigned', 'Assigned'),
        ('Dispatched', 'Dispatched'),
        ('InProgress', 'InProgress'),
        ('Incomplete', 'Incomplete'),
        ('Complete', 'Complete'),
        ('Cancelled', 'Cancelled'),
    ]
    scheduled = models.BooleanField(default=False)

    title = models.CharField(max_length=255, null=True, default='', blank=True)
    # Start_Date_Time = models.DateTimeField(default=timezone.now(), null=True, blank=True)
    # End_Date_Time = models.DateTimeField(default=timezone.now(), null=True, blank=True)
    # report_to_origin = models.DateTimeField(default=timezone.now(), null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=TRIP_STATUS, default='incomplete'
    )
    origin = models.ForeignKey(BasePlant, on_delete=models.CASCADE, null=True)
    staffNotes	= models.CharField(max_length=2048, null=True, default='', blank=True)
    driverNotes	= models.CharField(max_length=2048, null=True, default='', blank=True)
    shiftType = models.CharField(max_length=10,choices=[('Day','Day'),('Night','Night')], default='Day')
    
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    createdTime = models.TimeField(default=timezone.now(), null=True, blank=True)
    preStartWindow = models.CharField(max_length=2,default='15')
    stop = models.ForeignKey(Client, on_delete=models.CASCADE)
    
    startTime = models.TimeField(default=None, null=True, blank=True)
    endTime = models.TimeField(default=None, null=True, blank=True)
    reportingTime = models.TimeField(default=None, null=True, blank=True)
    
    startDate = models.DateField(default=None, null=True, blank=True)
    endDate = models.DateField(default=None, null=True, blank=True)
    
    recurringType = models.CharField(max_length=20, choices=[('NoRecurring','NoRecurring'),('Daily','Daily'),('Custom','Custom')], default='NoRecurring')
    sunday = models.BooleanField(default=False)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)

    def is_driver_available(self):
        leave_requests = self.driver.leaverequest_set.filter(
            start_date__lte=self.Start_Date_Time,
            end_date__gte=self.Start_Date_Time,
            status='Approved'
        )
        return not leave_requests.exists()
    
    def __str__(self):
        return self.title
    

class AppointmentTruck(models.Model):
    appointmentId = models.ForeignKey(Appointment,on_delete=models.CASCADE)
    truckNo = models.ForeignKey(AdminTruck,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.truckNo.adminTruckNumber)


class AppointmentDriver(models.Model):
    appointmentId = models.ForeignKey(Appointment,on_delete=models.CASCADE)
    driverName = models.ForeignKey(Driver,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.driverName.name)


class AppointmentStop(models.Model):
    appointmentId = models.ForeignKey(Appointment,on_delete=models.CASCADE, default=None)
    stopName = models.ForeignKey(BasePlant,on_delete=models.CASCADE)
    stopType = models.CharField(max_length=100,choices=[('Stop','Stop'),('Pickup','Pickup'),('Dropoff','Dropoff')], default="Stop") 
    arrivalTime = models.TimeField(null=True, blank=True)
    duration = models.PositiveBigIntegerField(default=0)
    notes = models.CharField(default='', null=True, max_length=2048)
    
    def __str__(self):
        return str(self.stopName.basePlant)


class PreStart(models.Model):
    preStartName = models.CharField(max_length=50, default='', null=True)
    createdDate = models.DateTimeField(default=None, null=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.preStartName)    
    
    # fitForWork = models.BooleanField(default = False)
    # vehicleStatus = models.BooleanField(default = False)
    # vehiclePaper = models.BooleanField(default = False)
    # curDate = models.DateTimeField(default=timezone.now())
    # comment = models.CharField(max_length = 1024, default='', null=True)
    # driver = models.ForeignKey(Driver, on_delete=models.CASCADE, default = None)
    
    # def __str__(self):
    #     return str("Driver is " + ("Fit" if self.fitForWork == True else "Not Fit"))
    
class PreStartQuestion(models.Model):
    QUESTION_TYPE = {
        ('Driver related','Driver related'),
        ('Vehicle related','Vehicle related'),
        ('Other','Other')        
    }
    questionText = models.CharField(max_length=1024, default='', null=True)
    questionType = models.CharField(max_length=20, choices=QUESTION_TYPE)
    preStartId = models.ForeignKey(PreStart, on_delete=models.CASCADE, default=None)
    
    # Four options for this question
    optionTxt1 = models.CharField(max_length=30, default='', null=True)
    wantFile1 = models.BooleanField(default=False)
    # optionFile1 = models.FileField(null=True, blank=True)
    # optionComment1 = models.CharField(max_length=1024, default='', null=True)
    
    optionTxt2 = models.CharField(max_length=30, null=True, blank=True)
    wantFile2 = models.BooleanField(default=False)
    # optionFile2 = models.FileField(null=True, blank=True)
    # optionComment2 = models.CharField(max_length=1024, default='', null=True)
   
    
    optionTxt3 = models.CharField(max_length=30, null=True, blank=True)
    wantFile3 = models.BooleanField(default=False)
    # optionFile3 = models.FileField(null=True, blank=True)
    # optionComment3 = models.CharField(max_length=1024, default='', null=True)
   
    
    optionTxt4 = models.CharField(max_length=30, null=True, blank=True)
    wantFile4 = models.BooleanField(default=False)
    # optionFile4 = models.FileField(null=True, blank=True)
    # optionComment4 = models.CharField(max_length=1024, default='', null=True)
    
    
    def __str__(self):
        return str(self.questionText) + '------' + str(self.preStartId)
    

class DriverPreStart(models.Model):
    shiftId = models.ForeignKey(DriverShift, on_delete=models.CASCADE, default=None, null=True)
    tripId = models.ForeignKey(DriverShiftTrip, on_delete=models.CASCADE, default=None, null=True)
    truckConnectionId =  models.ForeignKey(ClientTruckConnection, on_delete=models.CASCADE, default=None, null=True)
    clientId =  models.ForeignKey(Client, on_delete=models.CASCADE, default=None, null=True)
    preStartId =  models.ForeignKey(PreStart, on_delete=models.CASCADE, default=None, null=True)
    driverId =  models.ForeignKey(Driver, on_delete=models.CASCADE, default=None, null=True)
    curDateTime = models.DateTimeField(null=True)
    comment = models.CharField(max_length=2048, default='', null=True)

    def __str__(self):
        return str(self.driverId.name) + '-->' + str(self.curDateTime)
    
    
class DriverPreStartQuestion(models.Model):
    preStartId =  models.ForeignKey(DriverPreStart, on_delete=models.CASCADE, default=None, null=True)
    questionId =  models.ForeignKey(PreStartQuestion, on_delete=models.CASCADE, default=None, null=True)
    answer = models.CharField(max_length=255, default='', null=True)
    answerFile = models.FileField(default=None, null=True)
    comment = models.CharField(max_length=2048, default='', null=True)
    
    def __str__(self):
        return str(self.questionId.questionText) + '-->' + str(self.answer)

    
    
   
    
    
    
    
    
    

    