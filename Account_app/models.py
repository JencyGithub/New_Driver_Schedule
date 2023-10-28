from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator,RegexValidator
from datetime import date
from django.utils import timezone
from GearBox_app.models import *


# -----------------------------------
# Plants section
# -----------------------------------

class BasePlant(models.Model):
    basePlant = models.CharField(unique= True,max_length=200)

    def __str__(self) -> str:
        return str(self.basePlant)

# -----------------------------------
# Trips section
# -----------------------------------

class DriverTrip(models.Model):
    verified = models.BooleanField(default=False)
    driverId = models.ForeignKey(Driver, on_delete=models.CASCADE)
    clientName = models.ForeignKey(Client,on_delete=models.CASCADE)
    shiftType = models.CharField(max_length=200,choices=(('Day','Day'),('Night','Night')))
    numberOfLoads = models.FloatField(default=0)
    truckNo = models.IntegerField()
    shiftDate = models.DateField(null=True, default=None)
    startTime = models.CharField(max_length=200)
    endTime = models.CharField(max_length=200)
    loadSheet = models.FileField(upload_to='static/img/finalloadSheet')
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
    docketId = models.AutoField(primary_key=True)
    shiftDate = models.DateField(null=True, default=timezone.now())
    tripId = models.ForeignKey(DriverTrip, on_delete=models.CASCADE)
    docketNumber = models.IntegerField()
    docketFile = models.FileField(upload_to='static/img/docketFiles')
    basePlant = models.ForeignKey(BasePlant,on_delete=models.CASCADE)
    noOfKm = models.FloatField(default=0)
    transferKM = models.FloatField(default=0)
    returnToYard = models.BooleanField(default=False)
    tippingToYard = models.BooleanField(default=False)
    returnQty = models.FloatField(default=0)
    returnKm = models.FloatField(default=0)
    waitingTimeStart = models.CharField(max_length=200)
    waitingTimeEnd = models.CharField(max_length=200)
    totalWaitingInMinute = models.FloatField(default=0)
    surcharge_type = models.ForeignKey(Surcharge, on_delete=models.CASCADE)
    surcharge_duration = models.FloatField(default=0)
    cubicMl = models.FloatField(default=0)
    standByStartTime = models.CharField(max_length=200)
    standByEndTime = models.CharField(max_length=200)
    others = models.FloatField(default=0)
    comment = models.CharField(max_length=255, null=True, default='None')
    
    def __str__(self) -> str:
        return str(self.docketNumber)

    class Meta:
        unique_together = (('docketNumber', 'shiftDate'),)



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
    
    waitingTimeInMinutes = models.FloatField(max_length=255,default=0)
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
   
    others = models.CharField(max_length=255,default= '', null= True , blank=True)
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

# -----------------------------------
# Holiday section
# -----------------------------------
class PublicHoliday(models.Model):
    date = models.DateField()
    stateName = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return str(self.description)
    
    
 

