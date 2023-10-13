from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator,RegexValidator
from datetime import date
from django.utils import timezone
from GearBox_app.models import *


# -----------------------------------
# Plants section
# -----------------------------------

class BasePlant(models.Model):
    basePlant = models.CharField(primary_key=True, max_length=200)

    def __str__(self) -> str:
        return str(self.basePlant)
    


# -----------------------------------
# Trips section
# -----------------------------------

class DriverTrip(models.Model):
    verified = models.BooleanField(default=False)
    driverId = models.ForeignKey(Driver, on_delete=models.CASCADE)
    clientName = models.CharField(max_length=200)
    shiftType = models.CharField(max_length=200)
    numberOfLoads = models.IntegerField()
    truckNo = models.IntegerField()
    shiftDate = models.DateTimeField(null=True, default=None)
    startTime = models.CharField(max_length=200)
    endTime = models.CharField(max_length=200)
    logSheet = models.FileField(upload_to='static/img/finalLogSheet')
    comment = models.CharField(max_length=200, default='None')

    def __str__(self) -> str:
        return str(self.id)


class DriverDocket(models.Model):
        
    SURCHARGE_NATURE_CHOICES = (
        ('fixed normal', 'FIXED NORMAL'),
        ('fixed sunday', 'FIXED SUNDAY'),
        ('fixed public holiday', 'FIXED PUBLIC HOLIDAY'),
        ('per cubic meters normal', 'PER CUBIC METERS NORMAL'),
        ('per cubic meters sunday', 'PER CUBIC METERS SUNDAY'),
        ('per cubic meters public holiday', 'PER CUBIC METERS PUBLIC HOLIDAY'),
    )
    BASE_PLANTS_CHOICE = [('select','SELECT')]
    basePlants = BasePlant.objects.all()
    choices_list = BASE_PLANTS_CHOICE 
    for plant in basePlants:
        choices_list.append((plant.basePlant, plant.basePlant.upper())) 

    BASE_PLANTS_CHOICE = tuple(choices_list) 

    docketId = models.AutoField(primary_key=True)
    tripId = models.ForeignKey(DriverTrip, on_delete=models.CASCADE)
    shiftDate = models.DateTimeField(null=True, default=None)
    docketNumber = models.IntegerField()
    docketFile = models.FileField(upload_to='static/img/docketFiles')
    
    basePlant = models.CharField(
        max_length=31, choices=BASE_PLANTS_CHOICE, default='select')
    
    noOfKm = models.FloatField(default=0)
    transferKM = models.PositiveIntegerField(default=0)
    returnKm = models.FloatField(default=0)
    waitingTimeInMinutes = models.CharField(max_length=255)
    minimumLoad = models.FloatField(default=0)
    surcharge_type = models.CharField(
        max_length=31, choices=SURCHARGE_NATURE_CHOICES, default='fixed normal')
    surcharge_duration = models.FloatField(default=0)
    cubicMl = models.PositiveIntegerField(default=0)
    minLoad = models.PositiveIntegerField(default=0)
    standByPerHalfHourDuration = models.FloatField(default=0)
    others = models.PositiveIntegerField(default=0)

    # @property
    # def total_cost(self):
    #     return self.waitingTimeCost + self.transferKMSCost + self.cubicMlCost + self.minLoadCost + self.othersCost

    def __str__(self) -> str:
        return str(self.tripId)

    class Meta:
        unique_together = (('docketNumber', 'shiftDate'),)


class PastTrip(models.Model):
    SHIFT_CHOICES = (
        ('Day', 'Day'),
        ('Night', 'Night'),
    )

    Date = models.DateTimeField(null=True, default=None)
    Truck_No = models.CharField(max_length=255, null=True, default=None)
    Truck_Type = models.CharField(max_length=255, null=True, default=None)
    Replacement = models.CharField(max_length=255, null=True, default=None)
    Driver_Name = models.CharField(max_length=255, null=True, default=None)
    Docket_NO = models.CharField(max_length=255, null=True, default=None)
    Load_Time = models.DateTimeField(null=True, default=None)
    Return_time = models.DateTimeField(null=True, default=None)
    Load_qty = models.PositiveIntegerField(null=True, default=None)
    Doc_KMs = models.FloatField(null=True, default=None)
    Actual_KMs = models.FloatField(null=True, default=None)
    waiting_time_starts_Onsite = models.DateTimeField(null=True, default=None)
    waiting_time_end_offsite = models.DateTimeField(null=True, default=None)
    Total_minutes = models.IntegerField(null=True, default=None)
    Returned_Qty = models.PositiveIntegerField(null=True, default=None)
    Returned_KM = models.FloatField(null=True, default=None)
    Returned_to_Yard = models.BooleanField(null=True, default=None)
    Comment = models.TextField(null=True, default=None)
    Transfer_KM = models.FloatField(null=True, default=None)
    stand_by_Start_Time = models.DateTimeField(null=True, default=None)
    stand_by_end_time = models.DateTimeField(null=True, default=None)
    stand_by_total_minute = models.IntegerField(null=True, default=None)
    Stand_by_slot = models.CharField(max_length=255, null=True, default=None)
    category = models.CharField(max_length=255, null=True, default=None)
    call_out = models.CharField(max_length=255, null=True, default=None)
    standby_minute = models.IntegerField(null=True, default=None)
    ShiftType = models.CharField(
        max_length=5, choices=SHIFT_CHOICES, null=True, default=None)


class RCTI(models.Model):
    
    UNIT_CHOICES = (
        ('minute','MINUTE'),
        ('slot','SLOT'),
    )

    truckNo = models.FloatField(default=0)
    docketNumber = models.CharField( max_length=10,default='')
    docketDate = models.DateField()
    docketYard = models.CharField(default='', max_length=255)

    noOfKm = models.FloatField(default=0)
    cubicMl = models.FloatField(default=0)
    cubicMiAndKmsCost= models.FloatField(default=0)
    destination = models.CharField(max_length=255, default='Not given')
    cartageGSTPayable = models.FloatField(default=0)
    cartageTotalExGST = models.FloatField(default=0)
    cartageTotal = models.FloatField(default=0)
    
    transferKM = models.FloatField(default=0)
    transferKMCost = models.FloatField(default=0)
    transferKMGSTPayable = models.FloatField(default=0)
    transferKMTotalExGST = models.FloatField(default=0)
    transferKMTotal = models.FloatField(default=0)
    
    returnKm = models.FloatField(default=0)
    returnPerKmPerCubicMeterCost = models.FloatField(default=0)
    returnKmGSTPayable = models.FloatField(default=0)
    returnKmTotalExGST = models.FloatField(default=0)
    returnKmTotal = models.FloatField(default=0)
    
    waitingTimeSCHED = models.FloatField(default=0)
    waitingTimeSCHEDCost = models.FloatField(default=0)
    waitingTimeSCHEDGSTPayable = models.FloatField(default=0)
    waitingTimeSCHEDTotalExGST = models.FloatField(default=0)
    waitingTimeSCHEDTotal = models.FloatField(default=0)
    
    waitingTimeInMinutes = models.CharField(max_length=255)
    waitingTimeCost = models.FloatField(default=0)
    waitingTimeGSTPayable = models.FloatField(default=0)
    waitingTimeTotalExGST = models.FloatField(default=0)
    waitingTimeTotal = models.FloatField(default=0)
    
    standByPerHalfHourCost = models.FloatField(default=0)
    standByPerHalfHourDuration = models.FloatField(default=0)
    standByUnit = models.CharField(choices=UNIT_CHOICES,default="minute",max_length=6)
    standByGSTPayable = models.FloatField(default=0)
    standByTotalExGST = models.FloatField(default=0)
    standByTotal = models.FloatField(default=0)
    
    minimumLoad = models.FloatField(default=0)
    loadCost = models.FloatField(default=0)
    minimumLoadGSTPayable = models.FloatField(default=0)
    minimumLoadTotalExGST = models.FloatField(default=0)
    minimumLoadTotal = models.FloatField(default=0)
    
    surcharge_fixed_normal = models.FloatField(default=0)
    surcharge_fixed_sunday = models.FloatField(default=0)
    surcharge_fixed_public_holiday = models.FloatField(default=0)
    surcharge_per_cubic_meters_normal = models.FloatField(default=0)
    surcharge_per_cubic_meters_sunday = models.FloatField(default=0)
    surcharge_per_cubic_meters_public_holiday = models.FloatField(default=0)
    surcharge_duration = models.FloatField(default=0)
    surchargeUnit = models.CharField(choices=UNIT_CHOICES,default="minute",max_length=6)
    surchargeGSTPayable = models.FloatField(default=0)
    surchargeTotalExGST = models.FloatField(default=0)
    surchargeTotal = models.FloatField(default=0)
   
    others = models.CharField(max_length=255,default= '')
    othersCost = models.FloatField(default=0)
    othersGSTPayable = models.FloatField(default=0)
    othersTotalExGST = models.FloatField(default=0)
    othersTotal = models.FloatField(default=0)
    
    def _str_(self) -> str:
        return str(self.docketNumber) + str(self.truckNo)


class RCTIDocketAdjustment(models.Model):
    DocketNo = models.ForeignKey(RCTI, on_delete=models.CASCADE)
    noOfKm = models.FloatField(default=0)
    noOfKmCost = models.FloatField(default=0)

    transferKM = models.PositiveIntegerField(default=0)
    transferKMCost = models.FloatField(default=0)

    returnKm = models.FloatField(default=0)
    returnPerKmPerCubicMeterCost = models.FloatField(default=0)

    waitingTimeInMinutes = models.CharField(max_length=255)
    waitingTimeCost = models.FloatField(default=0)

    minimumLoad = models.FloatField(default=0)
    loadCost = models.FloatField(default=0)

    surcharge_fixed_normal = models.FloatField(default=0)
    surcharge_fixed_sunday = models.FloatField(default=0)
    surcharge_fixed_public_holiday = models.FloatField(default=0)
    surcharge_per_cubic_meters_normal = models.FloatField(default=0)
    surcharge_per_cubic_meters_sunday = models.FloatField(default=0)
    surcharge_per_cubic_meters_public_holiday = models.FloatField(default=0)
    surcharge_duration = models.FloatField(default=0)

    cubicMl = models.PositiveIntegerField(default=0)
    cubicMlCost = models.FloatField(default=0)

    minLoad = models.PositiveIntegerField(default=0)
    loadCost = models.FloatField(default=0)

    standByPerHalfHourCost = models.FloatField(default=0)
    standByPerHalfHourDuration = models.FloatField(default=0)

    others = models.PositiveIntegerField(default=0)
    othersCost = models.FloatField(default=0)

    GSTPayable = models.FloatField(default=0)
    TotalExGST = models.FloatField(default=0)
    Total = models.FloatField(default=0)

    @property
    def total_cost(self):
        return self.waitingTimeCost + self.transferKMSCost + self.cubicMlCost + self.minLoadCost + self.othersCost

