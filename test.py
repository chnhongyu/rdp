import pandas as pd
# import openpyxl
# import sys
# print(sys.executable)

Dataset = 'Running Dinner dataset 2021.xlsx'
Bewoners = pd.read_excel(Dataset, sheet_name = 'Bewoners')
Adressen = pd.read_excel(Dataset, sheet_name = 'Adressen')
Paar = pd.read_excel(Dataset, sheet_name = 'Paar blijft bij elkaar', header = 1)
Buren = pd.read_excel(Dataset, sheet_name = 'Buren', header = 1)
Kookte = pd.read_excel(Dataset, sheet_name = 'Kookte vorig jaar', header = 1)
Tafelgenoot = pd.read_excel(Dataset, sheet_name = 'Tafelgenoot vorig jaar', header = 1)

# verzamelingen
#A = all_sheets['Adressen']['Huisadres']
#D = all_sheets['Bewoners']['Bewoner']
#E = all_sheets['Paar blijft bij elkaar'][['Bewoner1', 'Bewoner2']]
#G = list('Voor', 'Hoofd', 'Na')

# parameters
#La = all_sheets['Adressen'][['Huisadres', 'Min groepsgrootte']]
#Ua = all_sheets['Adressen'][['Huisadres', 'Max groepsgrootte']]
