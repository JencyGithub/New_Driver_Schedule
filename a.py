import datetime 
import variables 
from django.core.mail import send_mail
import subprocess
import time


for i in range(10):
    # Replace with the path to your Python script
    script_path = r"F:/New_Driver_Schedule/scripts/preStartNotFilledService.py"
    subprocess.Popen(["python","manage.py" ,"runscript", 'sendEmailOnPreStartAndShiftEndNotFilled' , "--continue-on-error"])
    time.sleep(15)  # Execute every 15 Minutes

