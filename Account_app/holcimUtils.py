import re,sys,os, shutil , csv
# import pandas as pd
from datetime import datetime
# import matplotlib.pyplot as plt
import numpy as np


with open('static/Account/tempRCTIInvoice/PNR-9140-Sep-23.csv','r') as f:
    csv_reader = csv.reader(f)

    prepared_ = []
    count_ = 0
    for row in csv_reader:
        row =row[0].split('   ')
        for j in row:
            if j == '':
                row.remove(j)
                # prepared_.append(j)
        count_ +=1
        if count_ >2:
            print(row)