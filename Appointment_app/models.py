from django.db import models
from django.utils import timezone

from GearBox_app.models import *

class Appointment(models.Model):
    TRIP_STATUS = [
        ('unassigned', 'Unassigned'),
        ('assigned', 'Assigned'),
        ('dispacted', 'Dispatched'),
        ('in_progress', 'In Progress'),
        ('incomplete', 'Incomplete'),
        ('complete', 'Complete'),
        ('cancelled', 'Cancelled'),
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

    Report_Time = models.TimeField()
    Dwell_Time = models.TimeField()
    Block_Time = models.TimeField()
    Total_Time = models.TimeField()

    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    truckNo = models.IntegerField(default=0)
    # truckNo = models.ForeignKey(AdminTruck, on_delete=models.CASCADE)
    stop = models.ForeignKey(Client, on_delete=models.CASCADE)


    def is_driver_available(self):
        leave_requests = self.driver.leaverequest_set.filter(
            start_date__lte=self.Start_Date_Time,
            end_date__gte=self.Start_Date_Time,
            status='Approved'
        )
        return not leave_requests.exists()