# import csv 
# # from Trips_details_app.models import *
# import pandas as pd



# f = open("pastTripFileName.txt",'r')
# file_name = f.read()
# file_name, shift = file_name.split('(')[0], file_name.split('(')[-1][:-1].split(',')

# def dateConvert(date_):
#     date_ = date_.split('/')
#     year_ ='20' + date_[-1]
#     return year_ + '-' + date_[1] + '-' + date_[0]


# def insertIntoModel(dataList,shiftType):
#     print(dataList[1])
#     TripObj = PastTrip()
#     # Day shift
#     if 'dayShift' == str(shiftType):
#         TripObj.Truck_Type = dataList["Truck Type"]
#         TripObj.Replacement = dataList["Replacement"]
#         TripObj.Stand_by_slot = dataList["Stand by slot"]
#         TripObj.ShiftType = 'Day'
        
#     else:
#         # Night Shift
#         TripObj.category = dataList["Category"]
#         TripObj.call_out = dataList["Call Out"]
#         TripObj.standby_minute = dataList["Stand By Minutes"]
#         TripObj.ShiftType = 'Night'
        
    
#     TripObj.Date = str(str(dataList["Date"]).split()[0])
#     TripObj.Truck_No = dataList["Truck No."]
#     TripObj.Driver_Name = dataList["Driver's Name"]
#     TripObj.Docket_NO = dataList["Docket  NO "]
#     # TripObj.Load_Time = dataList["Load Time"]
#     TripObj.Load_Time = None
#     # TripObj.Return_time = dataList["Return time"]
#     TripObj.Return_time = None
#     TripObj.Load_qty = dataList["Load qty"]
#     TripObj.Doc_KMs = dataList["Doc KMs "]
#     TripObj.Actual_KMs = dataList["Actual KMs "]
#     # TripObj.waiting_time_starts_Onsite = dataList["waiting time starts (Onsite)"]
#     TripObj.waiting_time_starts_Onsite = None
#     # TripObj.waiting_time_end_offsite = dataList["waiting time end (offsite)"]
#     TripObj.waiting_time_end_offsite = None
#     TripObj.Total_minutes = dataList["Total mintes"]
#     TripObj.Returned_Qty = dataList["Returned Qty."]
#     TripObj.Returned_KM = dataList["Returned KM"]
#     TripObj.Returned_to_Yard = dataList["Returned to Yard"]
#     TripObj.Comment = dataList["Comment"]
#     TripObj.Transfer_KM = dataList["Transfer KM"]
#     # TripObj.stand_by_Start_Time = dataList["stand by Start Time"]
#     TripObj.stand_by_Start_Time = None
#     # TripObj.stand_by_end_time = dataList["stand by end time"]
#     TripObj.stand_by_end_time = None
#     TripObj.stand_by_total_minute = dataList["stand by total minute"]
#     TripObj.save()
    

# excel_file_path = f'static/img/pastTripFiles/{file_name}'
# excel_data = pd.read_excel(excel_file_path, sheet_name=None)
# sheet_names = list(excel_data.keys())

# for i in shift:
#     for j in sheet_names:
#         if i.lower() in j.lower().replace(' ',''):
#             df = pd.read_excel(excel_file_path, sheet_name=j)
#             # print(df.loc[1])
            
#             for index, row in df.iterrows():
#                 insertIntoModel(row,i)
#                 print('saved')
#                 exit()




