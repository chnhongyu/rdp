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

for i in d:
    abc= oplossing[oplossing['Bewoner']==i] [['Voor','Hoofd','Na']].values[0]
    l = len(set(abc))
    c1[i]= l 
#c1 returnt een dictionary, met 'bewoner': aantal verschillende adressen op de avond
# wat dus gelijk moet zijn aan 3, voor hoofd en na
# set() maakt het uniek

dfc1 = pd.DataFrame(list(c1.items()), columns=['Sleutel', 'Waarde'])

ongelijke_waarden = dfc1[dfc1['Waarde'] != 3]

# Als de DataFrame 'ongelijke_waarden' leeg is, betekent dit dat er geen 'Sleutel' is met een andere 'Waarde' dan 3
if ongelijke_waarden.empty:
    print("Alle 'Waarde'-waarden zijn gelijk aan 3.")
else:
    print("Er zijn 'Sleutel'-waarden met een andere 'Waarde' dan 3:")
    print(ongelijke_waarden)

