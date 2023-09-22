import pandas as pd
# import openpyxl
# import sys
# print(sys.executable)

Dataset = 'Running Dinner dataset 2021.xlsx'
Eerste_Oplossing = 'Running Dinner eerste oplossing 2021.xlsx'
Bewoners = pd.read_excel(Dataset, sheet_name = 'Bewoners')
Adressen = pd.read_excel(Dataset, sheet_name = 'Adressen')
Paar = pd.read_excel(Dataset, sheet_name = 'Paar blijft bij elkaar', header = 1)
Buren = pd.read_excel(Dataset, sheet_name = 'Buren', header = 1)
Kookte = pd.read_excel(Dataset, sheet_name = 'Kookte vorig jaar', header = 1)
Tafelgenoot = pd.read_excel(Dataset, sheet_name = 'Tafelgenoot vorig jaar', header = 1)
Oplossing = pd.read_excel(Eerste_Oplossing)

# verzamelingen
A = Adressen['Huisadres']
D = Bewoners['Bewoner']
E = Paar[['Bewoner1', 'Bewoner2']]
G = ['Voor', 'Hoofd', 'Na']

# parameters
#l_a = Adressen['Min groepsgrootte']
#u_a = Adressen['Max groepsgrootte']
h_ad = Bewoners[['Huisadres','Bewoner']]
v_ag = Adressen[['Huisadres','Voorkeur gang']]
vg_ag = Kookte[['Huisadres','Gang']]

# constraints
l_a = dict(zip(Adressen['Huisadres'], Adressen['Min groepsgrootte']))
u_a = dict(zip(Adressen['Huisadres'], Adressen['Max groepsgrootte']))
X_adg = {}

for d in Oplossing['Huisadres']:
    for a in Oplossing['Bewoner']:
        for g in Oplossing['kookt']:
            # Controleer of de bewoner d eet op huisadres a en gang g
            if ((Oplossing['Bewoner'] == d) & (Oplossing['Huisadres'] == a) & (Oplossing['kookt'] == g)).any():
                X_adg[(d, a, g)] = 1
            else:
                X_adg[(d, a, g)] = 0

print(X_adg)
    