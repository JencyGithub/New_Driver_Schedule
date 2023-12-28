import re,sys,os, shutil , csv
# import pandas as pd
from datetime import datetime
# import matplotlib.pyplot as plt
import numpy as np

def getFileName():
    if getattr(sys,'frozen',False):
        return input("Enter your CSV name: ")
    else:
        return input("Enter your CSV name: ")

def checkDate(date_):
    pattern = r'\d{2}/\d{2}/\d{2}'
    return True if re.fullmatch(pattern,date_) else False

def setLine(given_line, previous_line):
    custom_row =[]
    
    if re.match(docket_pattern, given_line[0]) or 'ADJUSTMEN' in given_line[0]:
        None
    elif checkDate(given_line[0]):
        given_line.insert(0,previous_line[0][0])
    else:     
        given_line.insert(0,previous_line[0][1])
        given_line.insert(0,previous_line[0][0])
               
    if len(given_line) == 10:
        custom_row.extend(given_line[:5]) 
    else:
        custom_row.extend(given_line[:4]) 
        
    numeric_part, *character_parts = given_line[-5].split()
    custom_row.extend([numeric_part, ' '.join(character_parts)]) 
    custom_row.extend(given_line[-4:])
    if len(custom_row) == 10:
        custom_row.insert(4,'')
        
    # if previous_line:
    if previous_line and custom_row[0] == previous_line[0][0]:
        res =   previous_line[0] + custom_row[1:]
        return res
    else:
        return custom_row

def setLineExpense(given_line, previous_line, truckNo , filePath):
    custom_row =[]
    
    # if re.match(docket_pattern, given_line[0]):
    #     None
    if checkDate(given_line[0]):
        if previous_line:
            given_line.insert(0,previous_line[1])
    elif checkDate(given_line[1]):
        pass
    else:  
        if previous_line:   
            given_line.insert(0,previous_line[2])
            given_line.insert(0,previous_line[1])
    
    if ' ' in given_line[2]:
        given_line.insert(2,'NOT SELECTED')
    
    if len(given_line) == 10:
        custom_row.extend(given_line[:5]) 
    else:
        custom_row.extend(given_line[:4]) 
        
    numeric_part, *character_parts = given_line[-5].split()
    custom_row.extend([numeric_part, ' '.join(character_parts)]) 
    custom_row.extend(given_line[-4:])
    if len(custom_row) == 10:
        custom_row.insert(4,'')
    
    custom_row.insert(0,truckNo) 
        
    
    if len(custom_row) < 11:
        return previous_line
    
    with open(filePath , 'a') as file:
        writer = csv.writer(file)
        writer.writerow(custom_row)
        
    return custom_row
        # if previous_line:
    # if previous_line and custom_row[0] == previous_line[0][0]:
    #     res =   previous_line[0] + custom_row[1:]
    #     return res
    # else:
    #     return custom_row


def appendToCsv(given_list,file_name,folder_name,truckNo):
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        for i in given_list:
            res = truckNo
            for j in i[0]:
                j = j.replace(',',' ')
                res = res + ',' + j
            res += '\n'
            # insertIntoModel(res)   
            with open('static/Account/RCTI/RCTIInvoice/'+file_name,'a') as f:
                f.write(res)
    except Exception as e:
        pass
        # rctiErrorObj = RctiErrors( 
        #                     docketNumber = None,
        #                     docketDate = None,
        #                     errorDescription = e,
        #                     fileName = file_name.split('/')[-1]
        # )
        # rctiErrorObj.save()        

# file_path = getFileName()
args = sys.argv[-1]
# args = '20231218124557@_!Boral-15-Apr-2023.csv'

# args ='20231120042226@_!Boral-15-Jan-2023.csv'
file_path = 'static/Account/RCTI/tempRCTIInvoice/' + args
# file_path = 'static/Account/RCTI/tempRCTIInvoice/20231218124557@_!Boral-15-Apr-2023.csv'

while(file_path[-4:] != '.csv'):
    print("Your given file is not valid.")
    file_path = getFileName()

# File name
converted_file = "converted_" + args
converted_file_expenses = "expenses_converted_" + args

with open ('static/Account/RCTI/RCTIInvoice/'+converted_file_expenses , 'a') as f:
    f.close()
    
with open("File_name_file.txt",'w+',encoding='utf-8') as f:
    f.write(f'{converted_file}<>{converted_file_expenses}')
    f.close()
    
folderName =  'static/Account/RCTI/RCTIInvoice'
# os.makedirs(folderName)
with open(folderName+'/'+converted_file,'a') as f:
    r = "Truck no.,Docket no.,Delivery Date, basePlant, Description, Paid Kms, Invoice QTY, Unit, Unit price, Total (Excl. GST), GST Payable, Total (Inc. GST),Delivery Date, basePlant, Description, Paid Kms, Invoice QTY, Unit, Unit price, Total (Excl. GST), GST Payable, Total (Inc. GST),Delivery Date, basePlant, Description, Paid Kms, Invoice QTY, Unit, Unit price, Total (Excl. GST), GST Payable, Total (Inc. GST),Delivery Date, basePlant, Description, Paid Kms, Invoice QTY, Unit, Unit price, Total (Excl. GST), GST Payable, Total (Inc. GST) \n" 
    f.write(r)
    f.close()
    res = ''


earnings_carter_list, earnings_temp, earnings_flag, expense_flag, key, earnings_carter_dic = [], [], False, False, None, {}

expense_carter_list = []
expense_carter_dic = {}
expense_temp = []

carter_no = r'(\d+)\s+Truck\s+(\w+)'
docket_pattern = r'^\d{8}$|^\d{6}$|^INV-\d+$'
line_no = 0
with open(file_path, 'r') as file:
    for line in file: 
        line_no += 1 
        if line_no == 187:
            pass
        if re.search(carter_no, line.replace(",",'').replace('Carter No:','').replace('"','').strip()):
            if earnings_carter_list != None and key != None and earnings_carter_list != []:
                earnings_carter_list.append(earnings_temp)
                earnings_temp = []
                earnings_carter_dic[truckNo] = earnings_carter_list
                # Appending into csv
                appendToCsv(earnings_carter_list,converted_file,folderName,truckNo)  
                        
                earnings_carter_list = []
                earnings_flag = False
                
            key = line.replace('Carter No:','').replace('"','').strip()
            truckNo = key.split(',')[1] 
            truckNo = truckNo.split()[-1]
            if re.match(r"^\d",truckNo) is None:
                truckNo = 0
                
        else:
            line_split_temp_ = re.split(r'\s{2,}', line)
            if ' ' in line_split_temp_[0] and (earnings_flag is True or expense_flag is True) and len(line_split_temp_) >= 7:
                line_split_temp_.insert(1,line_split_temp_[0].split(' ')[-1])
                line_split_temp_[0] = line_split_temp_[0].split(' ')[0]
                if 'ADJUSTMEN' not in line_split_temp_[0]:
                    line_split_temp_[0] = line_split_temp_[0]+ ' ' +line_split_temp_[1]
                    line_split_temp_.pop(1)
            # if len(line_split_temp_) < 2:
            #     line_split_temp_ = line_split_temp_.split(',')
            line_split_temp_[0],line_split_temp_[-1] = line_split_temp_[0][1:],line_split_temp_[-1][:-2]
            
            try:
                if line_split_temp_[0].lower() != 'docket' and line_split_temp_[0].lower() != 'no.':
                    if re.match(docket_pattern, line_split_temp_[0].replace(' ','')) and len(line_split_temp_) >= 7:
                        if earnings_temp:
                            earnings_carter_list.append(earnings_temp)
                            earnings_temp = []
                        line_split_temp_ = setLine(line_split_temp_,earnings_temp)
                        if  earnings_temp and earnings_temp[-1][0] == line_split_temp_[0]:
                                    del earnings_temp[0]
                        earnings_temp.append(line_split_temp_)
                    else:
                        if line_split_temp_[0].lower() not in ('"earnings', '"expenses', '"') and len(line_split_temp_) <= 1 and earnings_flag == True and re.match(r'^(?!"(po box|page)).*',line_split_temp_[0].lower()):    
                            earnings_temp[-1][3] = earnings_temp[-1][3] + line_split_temp_[0].replace('"',' ')
                            continue
                        elif line_split_temp_[0].lower() == '"earnings':
                            earnings_flag = True
                            expense_flag = False
                            continue
                        elif line_split_temp_[0].lower() == '"expenses':
                            earnings_flag = False
                            expense_flag = True
                            continue

                        if line_split_temp_[0].lower() == 'total earnings':
                            earnings_carter_list.append(earnings_temp)
                            earnings_temp = []
                            earnings_carter_dic[truckNo] = earnings_carter_list
                            # Appending into csv
                            appendToCsv(earnings_carter_list,converted_file,folderName,truckNo)
                            
                               
                            earnings_carter_list = []
                            earnings_flag = False 
                            key = None
                        elif earnings_flag == True and len(line_split_temp_) >= 7 and line_split_temp_[0].lower() != 'earnings':
                            
                            line_split_temp_ = setLine(line_split_temp_,earnings_temp)
                            
                            if  earnings_temp and earnings_temp[-1][0] == line_split_temp_[0]:
                                del earnings_temp[0]
                            earnings_temp.append(line_split_temp_)

                        elif expense_flag is True and line_split_temp_[0].lower() == 'total expenses':
                            expense_carter_list.append(expense_temp)
                            expense_temp = []
                            expense_carter_dic[truckNo] = expense_carter_list
                            # Appending into csv
                            appendToCsv(expense_carter_list,converted_file_expenses,folderName, truckNo )
                               
                            expense_carter_list = []
                            expense_flag = False 
                            key = None
                        elif expense_flag is True and len(line_split_temp_) >= 7 and 'expense' not in line_split_temp_[0].lower():
                            line_split_temp_ = setLineExpense(line_split_temp_,expense_temp,truckNo , folderName+'/'+converted_file_expenses)
                            expense_temp = line_split_temp_
                            # if expense_temp and expense_temp[-1][0] == line_split_temp_[0]:
                            #     del expense_temp[0]
                            # expense_temp.append(line_split_temp_)

            except Exception as e:
                with open("RctiConvertError.txt",'a') as f:
                    f.write("\n"+str(e) + ' ** ' + line)
                    
                # print(f'{e} at {line}')
                pass
            
    if earnings_carter_list:
        if earnings_temp:
            earnings_carter_list.append(earnings_temp)
        appendToCsv(earnings_carter_list,converted_file,folderName,truckNo)
    if expense_carter_list:
        if expense_temp:
            expense_carter_list.append(expense_temp)
        appendToCsv(expense_carter_list, converted_file_expenses, folderName, truckNo)
        
        


# -------------------------------------------------------------------------------------------------

# try:
#     directory_path = 'static/Account/RCTI/tempRCTIInvoice'
#     # Iterate over all items in the directory
#     for item in os.listdir(directory_path):
#         item_path = os.path.join(directory_path, item)

#         # Check if it's a file and delete it
#         if os.path.isfile(item_path):
#             os.remove(item_path)
#             # print(f"Deleted file: {item_path}")

#         # Check if it's a directory and delete it recursively
#         elif os.path.isdir(item_path):
#             shutil.rmtree(item_path)
#             # print(f"Deleted directory: {item_path}")

#     # print(f"All files and folders in '{directory_path}' have been deleted.")
# except Exception as e:
#     print(f"An error occurred: {str(e)}")
