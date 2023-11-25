import pandas as pd

pastData = pd.read_excel("test.xlsx")

print(pastData)
for key,row in pastData.iterrows():
    print(row[-2])
