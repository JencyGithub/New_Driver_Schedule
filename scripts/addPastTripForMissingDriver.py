from Account_app.models import *
from GearBox_app.models import *
from CRUD import *
from datetime import datetime
from Account_app.reconciliationUtils import  *
from datetime import time
import sys

matchingData = PastTripError.objects.filter(errorFromPastTrip="Driver matching query does not exist.", status=False)

arguments = sys.argv[1:] 

print(arguments)