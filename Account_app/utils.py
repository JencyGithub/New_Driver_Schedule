import re,sys,os, shutil
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

print("here")

def getFileName():
    if getattr(sys,'frozen',False):
        return input("Enter your CSV name: ")
    else:
        return input("Enter your CSV name: ")

def checkDate(date_):
    pattern = r'\d{2}/\d{2}/\d{2}'
    return True if re.fullmatch(pattern,date_) else False

def setLine(given_line,previous_line):
    custom_row =[]
    
    if re.match(docket_pattern, given_line[0]):
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


def appendToCsv(given_list,file_name,folder_name,truckNo):
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
            f.close()
            # res = ''

# file_path = getFileName()
args = sys.argv[-1]

# args ='20231009125409@_!pdf.csv'
file_path = 'static/Account/RCTI/tempRCTIInvoice/' + args

while(file_path[-4:] != '.csv'):
    print("Your given file is not valid.")
    file_path = getFileName()

# File name
converted_file = "converted_" + args

with open("File_name_file.txt",'w') as f:
    f.write(converted_file)
    f.close()

folderName =  'static/Account/RCTI/RCTIInvoice'
# os.makedirs(folderName)
with open(folderName+'/'+converted_file,'a') as f:
    r = "Truck no.,Docket no.,Delivery Date, basePlant, Description, Paid Kms, Invoice QTY, Unit, Unit price, Total (Excl. GST), GST Payable, Total (Inc. GST),Delivery Date, basePlant, Description, Paid Kms, Invoice QTY, Unit, Unit price, Total (Excl. GST), GST Payable, Total (Inc. GST),Delivery Date, basePlant, Description, Paid Kms, Invoice QTY, Unit, Unit price, Total (Excl. GST), GST Payable, Total (Inc. GST),Delivery Date, basePlant, Description, Paid Kms, Invoice QTY, Unit, Unit price, Total (Excl. GST), GST Payable, Total (Inc. GST) \n" 
    f.write(r)
    f.close()
    res = ''


earnings_carter_list, earnings_temp, earnings_flag, expense_flag, key, earnings_carter_dic = [], [], False, False, None, {}

carter_no = r'(\d+)\s+Truck\s+(\w+)'
docket_pattern = r'^\d{8}$|^\d{6}$'

with open(file_path, 'r') as file:
    for line in file:  
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
        else:
            line_split_temp_ = re.split(r'\s{2,}', line)
            # if len(line_split_temp_) < 2:
            #     line_split_temp_ = line_split_temp_.split(',')
            line_split_temp_[0],line_split_temp_[-1] = line_split_temp_[0][1:],line_split_temp_[-1][:-2]
            
            try:
                if line_split_temp_[0].lower() != 'docket' and line_split_temp_[0].lower() != 'no.':
                    if re.match(docket_pattern, line_split_temp_[0]):
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
                        elif len(line_split_temp_) >= 7 and line_split_temp_[0].lower() != 'earnings':
                            if earnings_flag == True:
                                line_split_temp_ = setLine(line_split_temp_,earnings_temp)
                                
                                if  earnings_temp and earnings_temp[-1][0] == line_split_temp_[0]:
                                    del earnings_temp[0]
                                earnings_temp.append(line_split_temp_)
            except Exception as e:
                print(f'{e} at {line}')
                pass


# -------------------------------------------------------------------------------------------------

try:
    directory_path = 'static/Account/RCTI/tempRCTIInvoice'
    # Iterate over all items in the directory
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)

        # Check if it's a file and delete it
        if os.path.isfile(item_path):
            os.remove(item_path)
            # print(f"Deleted file: {item_path}")

        # Check if it's a directory and delete it recursively
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
            # print(f"Deleted directory: {item_path}")

    # print(f"All files and folders in '{directory_path}' have been deleted.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
