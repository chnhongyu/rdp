import pandas as pd
# import openpyxl
# import sys
# print(sys.executable)

#inlezen data
Dataset = 'Running Dinner dataset 2021.xlsx'
Bewoners = pd.read_excel(Dataset, sheet_name = 'Bewoners')
Adressen = pd.read_excel(Dataset, sheet_name = 'Adressen')
Paar = pd.read_excel(Dataset, sheet_name = 'Paar blijft bij elkaar', header = 1)
Buren = pd.read_excel(Dataset, sheet_name = 'Buren', header = 1)
Kookte = pd.read_excel(Dataset, sheet_name = 'Kookte vorig jaar', header = 1)
Tafelgenoot = pd.read_excel(Dataset, sheet_name = 'Tafelgenoot vorig jaar', header = 1)

#inlezen input
Dataset2 = 'Running Dinner eerste oplossing 2021.xlsx'


# verzamelingen
A = Adressen['Huisadres']
D = Bewoners['Bewoner']
E = Paar[['Bewoner1', 'Bewoner2']]
G = ['Voor', 'Hoofd', 'Na']
print(A, D, E, G)

#parameters
k_a = 