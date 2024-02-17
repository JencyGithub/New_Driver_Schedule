from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator,RegexValidator
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User


TRUCK_TYPE_CHOICES = (
    ('Embedded','Embedded'),
    ('Casual','Casual'),
    
)
# -----------------------------------
# Client section
# -----------------------------------

class Client(models.Model):
    clientId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=255,default=None, null=True, blank=True)
    docketGiven = models.BooleanField(default=False)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self) -> str:
        return str(self.name) 

class ClientOffice(models.Model):
    clientId = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    locationType = models.CharField(max_length=10, choices=(('Home', 'Home'), ('Workplace', 'Workplace')))
    description = models.CharField(max_length=2048, default='', null=True)
    address1 = models.CharField(max_length=1024, null=True, default='')
    address2 = models.CharField(max_length=1024, null=True, default='')
    personName = models.CharField(max_length=100, null=True, default='')
    city = models.CharField(max_length=100, null=True, default='')
    state = models.CharField(max_length=100, null=True, default='')
    country = models.CharField(max_length=100, null=True, default='')
    postalCode = models.IntegerField(null=True, default=0)
    primaryContact = models.IntegerField(null=True, default=0)
    alternativeContact = models.IntegerField(null=True, default=0)

    def __str__(self) -> str:
        return str(self.description) + str(self.clientId) + str(self.locationType)

    

    
# -----------------------------------
# Rate Card
# -----------------------------------   

SURCHARGE_NATURE_CHOICES = (
    ('fixed normal', 'FIXED NORMAL'),
    ('fixed sunday', 'FIXED SUNDAY'),
    ('fixed public holiday', 'FIXED PUBLIC HOLIDAY'),
    ('per cubic meters normal', 'PER CUBIC METERS NORMAL'),
    ('per cubic meters sunday', 'PER CUBIC METERS SUNDAY'),
    ('per cubic meters public holiday', 'PER CUBIC METERS PUBLIC HOLIDAY'),
                           )

standby_time_grace_options = (
    ('per min cost', 'PER MIN COST'),
    ('slots', 'SLOTS')
)

class RateCard(models.Model):
    rate_card_name = models.CharField(max_length=255 , unique=True)
    tds = models.FloatField(default=0)
    clientName = models.ForeignKey(Client,on_delete=models.CASCADE , null=True)
    clientOfc = models.ForeignKey(ClientOffice,on_delete=models.CASCADE , null=True)

    def __str__(self) -> str:
        return str(self.rate_card_name)

class Surcharge(models.Model):
    surcharge_Name = models.CharField(max_length=255)
    # createdBy = models.ForeignKey('auth.user', on_delete=models.CASCADE, default=None)

    
    def __str__(self) -> str:
        return str(self.surcharge_Name)
    
class CostParameters(models.Model):
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    rate_card_name = models.ForeignKey(RateCard, on_delete=models.CASCADE)
    loading_cost_per_cubic_meter = models.FloatField(default=0)
    km_cost = models.FloatField(default=0)
    # surcharge_type = models.ForeignKey(Surcharge, on_delete=models.CASCADE)
    # surcharge_cost = models.FloatField(default=0)
    transfer_cost = models.FloatField(default=0)
    return_load_cost = models.FloatField(default=0)     # change name added
    return_km_cost = models.FloatField(default=0)       # new added
    standby_time_slot_size = models.PositiveIntegerField(default=0)
    standby_cost_per_slot = models.FloatField(default=0)
    waiting_cost_per_minute = models.FloatField(default=0)
    call_out_fees = models.FloatField(default=0)
    demurrage_fees = models.FloatField(default=0)
    cancellation_fees = models.FloatField(default=0) 
    clientPayableGst = models.FloatField(default=10.0)
    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(default=timezone.now() + timezone.timedelta(days=365*10), null=True, blank=True)

class RateCardSurchargeValue(models.Model):
    # createdBy = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    rate_card_name = models.ForeignKey(RateCard, on_delete=models.CASCADE)
    surcharge = models.ForeignKey(Surcharge, on_delete=models.CASCADE)
    surchargeValue = models.FloatField(default=0)
    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(default=timezone.now() + timezone.timedelta(days=365*10), null=True, blank=True)

    def __str__(self) -> str:
        return str(self.rate_card_name)
class ThresholdDayShift(models.Model):
    rate_card_name = models.ForeignKey(RateCard, on_delete=models.CASCADE)
    threshold_amount_per_day_shift = models.FloatField(default=0)
    loading_cost_per_cubic_meter_included = models.BooleanField(default=False)
    km_cost_included = models.BooleanField(default=False)
    surcharge_included  = models.BooleanField(default=False)

    # surcharge_fixed_normal_cost_included = models.BooleanField(default=False)
    # surcharge_fixed_sunday_cost_included = models.BooleanField(default=False)
    # surcharge_fixed_public_holiday_cost_included = models.BooleanField(default=False)
    # surcharge_per_cubic_meters_normal_cost_included = models.BooleanField(default=False)
    # surcharge_per_cubic_meters_sunday_cost_included = models.BooleanField(default=False)
    # surcharge_per_cubic_meters_public_holiday_cost_included = models.BooleanField(default=False)
    
    transfer_cost_included = models.BooleanField(default=False)
    return_cost_included = models.BooleanField(default=False)
    standby_cost_included = models.BooleanField(default=False)
    waiting_cost_included = models.BooleanField(default=False)
    call_out_fees_included = models.BooleanField(default=False)
    # demurrage_fees_included = models.BooleanField(default=False)

    min_load_in_cubic_meters = models.FloatField(default=0)
    min_load_in_cubic_meters_return_to_yard = models.FloatField(default=0)
    # min_load_in_cubic_meters_trip = models.FloatField(default=0)
     
    return_to_yard_grace = models.FloatField(default=0)         # new added
    return_to_tipping_grace = models.FloatField(default=0)      # new added

    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(default=timezone.now() + timezone.timedelta(days=365*10), null=True, blank=True)


class ThresholdNightShift(models.Model):
    rate_card_name = models.ForeignKey(RateCard, on_delete=models.CASCADE)
    threshold_amount_per_night_shift = models.FloatField(default=0)
    loading_cost_per_cubic_meter_included = models.BooleanField(default=False)
    km_cost_included = models.BooleanField(default=False)
    surcharge_included  = models.BooleanField(default=False)
    transfer_cost_included = models.BooleanField(default=False)
    return_cost_included = models.BooleanField(default=False)
    standby_cost_included = models.BooleanField(default=False)
    waiting_cost_included = models.BooleanField(default=False)
    call_out_fees_included = models.BooleanField(default=False)

    min_load_in_cubic_meters = models.FloatField(default=0)
    min_load_in_cubic_meters_return_to_yard = models.FloatField(default=0)

    return_to_yard_grace = models.FloatField(default=0)         # new added
    return_to_tipping_grace = models.FloatField(default=0)      # new added

    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(default=timezone.now() + timezone.timedelta(days=365*10), null=True, blank=True)


class Grace(models.Model):
    rate_card_name = models.ForeignKey(RateCard, on_delete=models.CASCADE)
    load_km_grace = models.FloatField(default=0)
    transfer_km_grace = models.FloatField(default=0)
    return_km_grace = models.FloatField(default=0)
    standby_time_grace_in_minutes = models.FloatField(default=0)
    chargeable_standby_time_starts_after = models.FloatField(default=0)
    waiting_time_grace_in_minutes = models.FloatField(default=0)
    chargeable_waiting_time_starts_after = models.FloatField(default=0)
    waiting_load_calculated_on_load_size = models.BooleanField(default=False)
    waiting_time_grace_per_cubic_meter = models.FloatField(default=0)
    waiting_grace_per_cubic_meter = models.FloatField(default=0)

    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(default=timezone.now() + timezone.timedelta(days=365*10), null=True, blank=True)

class OnLease(models.Model):
    rate_card_name = models.ForeignKey(RateCard, on_delete=models.CASCADE)
    hourly_subscription_charge = models.FloatField(default=0)
    daily_subscription_charge = models.FloatField(default=0)
    weekly_subscription_charge = models.FloatField(default=0)
    # quarterly_subscription_charge = models.FloatField(default=0)
    over_time_charge = models.FloatField(default=0) 
    surcharge_included  = models.BooleanField(default=True)
    transfer_cost_applicable = models.BooleanField(default=True)
    return_cost_applicable = models.BooleanField(default=True)
    standby_cost_per_slot_applicable = models.BooleanField(default=True)
    waiting_cost_per_minute_applicable = models.BooleanField(default=True)
    call_out_fees_applicable = models.BooleanField(default=True)
    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(default=timezone.now() + timezone.timedelta(days=365*10), null=True, blank=True)
    





    
# -----------------------------------
# Trucks section
# -----------------------------------



# -----------------------------------
# Truck Gearbox section
# -----------------------------------

# INFORMATION TAB
class TruckInformation(models.Model):
    fleet = models.CharField(max_length=100)
    group = models.PositiveSmallIntegerField(default=0)
    subGroup = models.PositiveSmallIntegerField(default=0)
    vehicleType = models.CharField(max_length=100, default='', null=True, blank=True)
    serviceGroup = models.CharField(max_length=100, default='', null=True, blank=True)
    truckImg1 = models.FileField(null=True, blank=True)
    truckImg2 = models.FileField(null=True, blank=True)
    truckImg3 = models.FileField(null=True, blank=True)
    informationMake = models.CharField(max_length=100, default='', null=True, blank=True)
    informationModel = models.CharField(max_length=100, default='', null=True, blank=True)
    informationConfiguration = models.CharField(max_length=100, default='', null=True, blank=True)
    informationChassis = models.CharField(max_length=100, default='', null=True, blank=True)
    informationBuildYear = models.PositiveIntegerField(default=0)
    
    informationIcon = models.CharField(max_length=100, default='', null=True, blank=True)
    customFieldLabel1 = models.CharField(max_length=100, default='', null=True, blank=True)
    customFieldLabel2 = models.CharField(max_length=100, default='', null=True, blank=True)
    customFieldLabel3 = models.CharField(max_length=100, default='', null=True, blank=True)
    customFieldLabel4 = models.CharField(max_length=100, default='', null=True, blank=True)
    customFieldLabel5 = models.CharField(max_length=100, default='', null=True, blank=True)
    customFieldLabel6 = models.CharField(max_length=100, default='', null=True, blank=True)
    customFieldValue1 = models.CharField(max_length=100, default='', null=True, blank=True)
    customFieldValue2 = models.CharField(max_length=100, default='', null=True, blank=True)
    customFieldValue3 = models.CharField(max_length=100, default='', null=True, blank=True)
    customFieldValue4 = models.CharField(max_length=100, default='', null=True, blank=True)
    customFieldValue5 = models.CharField(max_length=100, default='', null=True, blank=True)
    customFieldValue6 = models.CharField(max_length=100, default='', null=True, blank=True)

    registered = models.BooleanField(default=True)
    registration = models.CharField(max_length=100, default='', null=True, blank=True)
    registrationCode = models.CharField(max_length=100, default='', null=True, blank=True)
    registrationState = models.CharField(max_length=100, default='', null=True, blank=True)
    registrationDueDate = models.DateField(null=True, blank=True)
    registrationInterval = models.CharField(max_length=100, default='', null=True, blank=True)
    powered = models.BooleanField(default=False)
    engine = models.CharField(max_length=100, default='', null=True, blank=True)
    engineMake = models.CharField(max_length=100, default='', null=True, blank=True)
    engineModel = models.CharField(max_length=100, default='', null=True, blank=True)
    engineCapacity = models.CharField(max_length=100, default='', null=True, blank=True)
    engineGearBox = models.CharField(max_length=100, default='', null=True, blank=True)

    def __str__(self):
        return str(self.id)
    
class TruckInformationCustom(models.Model):
    customFieldLabel = models.CharField(max_length=100, default='', null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
# AXLES TAB
class Axles(models.Model):
    AXLES_CHOICES = (
        (0, 'None'),
        (1, 'Single'),
        (2, 'Dual'),
        (3, 'Triple'),
        (4, 'Quad'),
    )
    vehicle_axle1 = models.IntegerField(choices=AXLES_CHOICES, default=0)
    axle_make1 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_rims1 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_tyre_size1 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_suspensions1 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_brakes1 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_slack_adjusters1 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_differential1 =models.CharField(max_length=100, default='', null=True, blank=True)
    
    vehicle_axle2 = models.IntegerField(choices=AXLES_CHOICES, default=0)
    axle_make2 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_rims2 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_tyre_size2 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_suspensions2 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_brakes2 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_slack_adjusters2 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_differential2 =models.CharField(max_length=100, default='', null=True, blank=True)
    
    vehicle_axle3 = models.IntegerField(choices=AXLES_CHOICES, default=0)
    axle_make3 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_rims3 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_tyre_size3 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_suspensions3 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_brakes3 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_slack_adjusters3 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_differential3 =models.CharField(max_length=100, default='', null=True, blank=True)
    
    vehicle_axle4 = models.IntegerField(choices=AXLES_CHOICES, default=0)
    axle_make4 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_rims4 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_tyre_size4 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_suspensions4 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_brakes4 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_slack_adjusters4 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_differential4 =models.CharField(max_length=100, default='', null=True, blank=True)
    
    vehicle_axle5 = models.IntegerField(choices=AXLES_CHOICES, default=0)
    axle_make5 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_rims5 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_tyre_size5 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_suspensions5 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_brakes5 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_slack_adjusters5 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_differential5 =models.CharField(max_length=100, default='', null=True, blank=True)

    vehicle_axle6 = models.IntegerField(choices=AXLES_CHOICES, default=0)
    axle_make6 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_rims6 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_tyre_size6 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_suspensions6 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_brakes6 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_slack_adjusters6 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_differential6 =models.CharField(max_length=100, default='', null=True, blank=True)

    vehicle_axle7 = models.IntegerField(choices=AXLES_CHOICES, default=0)
    axle_make7 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_rims7 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_tyre_size7 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_suspensions7 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_brakes7 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_slack_adjusters7 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_differential7 =models.CharField(max_length=100, default='', null=True, blank=True)

    vehicle_axle8 = models.IntegerField(choices=AXLES_CHOICES, default=0)
    axle_make8 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_rims8 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_tyre_size8 = models.CharField(max_length=100, default='', null=True, blank=True)
    axle_suspensions8 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_brakes8 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_slack_adjusters8 =models.CharField(max_length=100, default='', null=True, blank=True)
    axle_differential8 =models.CharField(max_length=100, default='', null=True, blank=True)

    
    def _str_(self):
            return str(self.id)

#SETTINGS TAB
# class Settings(models.Model):

class AdminTruck(models.Model):
    # adminTruckNumber = models.PositiveIntegerField(validators=[MaxValueValidator(999999),MinValueValidator(100000)], unique=True)
    adminTruckNumber = models.PositiveIntegerField(unique=True)
    truckInformation = models.ForeignKey(TruckInformation, on_delete = models.CASCADE , null = True)
    truckAxles = models.ForeignKey(Axles, on_delete = models.CASCADE , null = True)
    truckActive = models.BooleanField(default=False)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return str(self.adminTruckNumber)
    
class Driver(models.Model):
    # driverId = models.IntegerField(primary_key=True, unique=True, default=generate_4digit_unique_key, editable=False)
    driverId = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    
    firstName = models.CharField(max_length=100, default='', null=True)
    middleName = models.CharField(max_length=100, default='', null=True)
    lastName = models.CharField(max_length=100, default='', null=True)
    
    def __str__(self) -> str:
        return str(self.driverId) + str(self.name)
        

class ClientTruckConnection(models.Model):
    truckNumber = models.ForeignKey(AdminTruck, on_delete=models.CASCADE)
    truckType = models.CharField(max_length=254 , choices=TRUCK_TYPE_CHOICES, default='Embedded')
    rate_card_name = models.ForeignKey(RateCard, on_delete=models.CASCADE)
    pre_start_name = models.PositiveIntegerField(default=0)
    clientId = models.ForeignKey(Client, on_delete=models.CASCADE)
    clientTruckId = models.PositiveIntegerField(default=0)
    basePlantId = models.PositiveIntegerField(default=0)  
    # clientTruckId = models.PositiveIntegerField(validators=[MaxValueValidator(999999)])  
    startDate = models.DateField(default=timezone.now())  
    endDate = models.DateField(null=True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, default=None)


    def __str__(self):
        return str(self.truckNumber) + str(self.clientId)
    
# -----------------------------------
# Leave section
# -----------------------------------

class NatureOfLeave(models.Model):
    reason = models.CharField(max_length=200)
    
    def __str__(self) -> str:
            return str(self.reason)

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, default=None)
    end_date = models.DateField(null=True, default=None)
    reason = models.ForeignKey(NatureOfLeave,on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied'), ('Cancel', 'Cancel')], default='Pending')
    # Add other fields as needed

    comment = models.CharField(max_length=2048, default='', null=True, blank=True)
    closedBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 

    def __str__(self):
        return f"{self.employee} - {self.start_date} to {self.end_date}"

# -----------------------------------
# Group
# -----------------------------------
    
class TruckGroup(models.Model):
    name = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.name



# DOCUMENTS TAB
class TruckDocument(models.Model):
    tags = models.CharField(max_length=300)
    filePath = models.FileField(upload_to='static/GearBox/document')
    description = models.TextField()
    
    def __str__(self):
        return str(self.tags)
    