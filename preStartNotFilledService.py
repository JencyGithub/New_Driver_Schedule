import os
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess

class PreStartNotFilledService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PreStartNotFilledService"
    _svc_display_name_ = "Pre-StartNotFilledService"
    _svc_description_ = "A service which runs periodically to send email for drivers who have not filled pre-start or end day shift."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        for i in range(10):
            # Replace with the path to your Python script
            script_path = r"F:/New_Driver_Schedule/scripts/preStartNotFilledService.py"
            subprocess.Popen(["python","manage.py" ,"runscript", 'sendEmailOnPreStartAndShiftEndNotFilled' , "--continue-on-error"])
            time.sleep(15)  # Execute every 15 Minutes
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PreStartNotFilledService)
