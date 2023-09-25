import pandas as pd

import pandas as pd 
from Constraint5 import Constraint5

Oplossing2021Excel = 'Running Dinner eerste oplossing 2021.xlsx'
Oplossing2021 = pd.read_excel(Oplossing2021Excel)

Dataset2021Excel = 'Running Dinner dataset 2021.xlsx'
Bewoners2021 = pd.read_excel(Dataset2021Excel, sheet_name = 'Bewoners')
Adressen2021 = pd.read_excel(Dataset2021Excel, sheet_name = 'Adressen')
Paar2021 = pd.read_excel(Dataset2021Excel, sheet_name = 'Paar blijft bij elkaar', header = 1)
Buren2021 = pd.read_excel(Dataset2021Excel, sheet_name = 'Buren', header = 1)
Kookte2021 = pd.read_excel(Dataset2021Excel, sheet_name = 'Kookte vorig jaar', header = 1)
Tafelgenoot2021 = pd.read_excel(Dataset2021Excel, sheet_name = 'Tafelgenoot vorig jaar', header = 1)

#-----------------------------
# Oplossing2022Excel = 'Running Dinner eerste oplossing 2022.xlsx'
# Oplossing2022 = pd.read_excel(Oplossing2022Excel)

# Dataset2022Excel = 'Running Dinner dataset 2022.xlsx'
# Bewoners2022 = pd.read_excel(Dataset2022Excel, sheet_name = 'Bewoners')
# Adressen2022 = pd.read_excel(Dataset2021Excel, sheet_name = 'Adressen')
# Paar2022 = pd.read_excel(Dataset2022Excel, sheet_name = 'Paar blijft bij elkaar', header = 1)
# Buren2022 = pd.read_excel(Dataset2022Excel, sheet_name = 'Buren', header = 1)
# Kookte2022 = pd.read_excel(Dataset2022Excel, sheet_name = 'Kookte vorig jaar', header = 1)
# Tafelgenoot2022 = pd.read_excel(Dataset2022Excel, sheet_name = 'Tafelgenoot vorig jaar', header = 1)

#------------------------------
# Constraint 1 zorgt voor dat elke deelnemer, elke gang, op 1 adres eet.
# dus deelnemer1: | a1 | a2 | a3 |
# input: Oplossing2021
# output: voldoet wel/niet aan constraint1

def constraint1(Oplossing):
    ### Oplossing is de dataframe van dat jaar. bijv Oplossing = pd.read_excel('.xlsx')###
    #functie checkt of de data voldoet aan constraint1, als statement True is voldoet het. False voldoet dus niet.
    statement = True

    Deelnemer_ongelijk_aan_3 = {}
    for deelnemer in Oplossing['Bewoner']:
        gangen = Oplossing[Oplossing['Bewoner']==deelnemer][['Voor','Hoofd','Na']].values[0]
        aantal_gangen = len(set(gangen))
        if aantal_gangen !=3:
            Deelnemer_ongelijk_aan_3[deelnemer]= aantal_gangen
    if len(Deelnemer_ongelijk_aan_3) >0:
        statement = False
    return print(statement)


constraint1(Oplossing2021)
    


