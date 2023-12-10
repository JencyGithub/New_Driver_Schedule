from django.db import models
from django.utils import timezone

from GearBox_app.models import *

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

    Title = models.CharField(max_length=255)
    Start_Date_Time = models.DateTimeField(default=timezone.now())
    End_Date_Time = models.DateTimeField(default=timezone.now())
    report_to_origin = models.DateTimeField(default=timezone.now())
    Status = models.CharField(
        max_length=20, choices=TRIP_STATUS, default='incomplete'
    )
    Origin = models.CharField(max_length=255)
    Recurring = models.CharField(max_length=255)
    Staff_Notes	= models.CharField(max_length=1024)
    
    Created_by = models.CharField(max_length=255)
    Created_time = models.TimeField(default=timezone.now())
    preStartWindow = models.CharField(max_length=2,default='15')

    # preStart_Time = models.DateTimeField(default=Start_Date_Time-preStartWindow)
    # Report_Time = models.TimeField()
    # Dwell_Time = models.TimeField()
    # Block_Time = models.TimeField()
    # Total_Time = models.TimeField()

    # driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    # truckNo = models.IntegerField(default=0)
    # truckNo = models.ForeignKey(AdminTruck, on_delete=models.CASCADE)
    stop = models.ForeignKey(Client, on_delete=models.CASCADE)


    def is_driver_available(self):
        leave_requests = self.driver.leaverequest_set.filter(
            start_date__lte=self.Start_Date_Time,
            end_date__gte=self.Start_Date_Time,
            status='Approved'
        )
        return not leave_requests.exists()
    
    def __str__(self):
        return self.Title
    
    

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

