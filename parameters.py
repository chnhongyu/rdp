import pandas as pd

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
oplossing = pd.read_excel(Dataset2)


# verzamelingen
A = Adressen['Huisadres']
D = Bewoners['Bewoner']
E = Paar[['Bewoner1', 'Bewoner2']]
G = ['Voor', 'Hoofd', 'Na']

#parameters
# ka = ?
l_a = Adressen['Min groepsgrootte']
u_a = Adressen['Max groepsgrootte']
h_ad = Bewoners[ ['Huisadres','Bewoner'] ]
v_ag = Adressen[ ['Huisadres','Voorkeur gang'] ]
vg_ag = Kookte[ ['Huisadres','Gang'] ]
vt_d1d2 = Tafelgenoot
b_d1d2 = Buren

#Elke DEELNEMER, Elke GANG, = 1
c1 = {}
d = set(oplossing['Bewoner'])
a = set(oplossing['Huisadres'])
g = set(oplossing['kookt'])
for i in g:
    print(i)

