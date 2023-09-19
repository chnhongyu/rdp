import pandas as pd
import pulp as pp

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
df2 = pd.read_excel(Dataset2)


# verzamelingen
A = Adressen['Huisadres']
D = Bewoners['Bewoner']
E = Paar[['Bewoner1', 'Bewoner2']]
G = ['Voor', 'Hoofd', 'Na']
# print(A, D, E, G)

#parameters
# ka = ?
l_a = Adressen['Min groepsgrootte']
u_a = Adressen['Max groepsgrootte']
h_ad = Bewoners[ ['Huisadres','Bewoner'] ]
v_ag = Adressen[ ['Huisadres','Voorkeur gang'] ]
vg_ag = Kookte[ ['Huisadres','Gang'] ]
vt_d1d2 = Tafelgenoot
b_d1d2 = Buren

#Er moet gelden dat

#elk deelnemer woont op precies een adres, sum(a,h_ad)=1 for all d

