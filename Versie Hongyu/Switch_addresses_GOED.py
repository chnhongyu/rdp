import pandas as pd
import numpy as np
import random 

dataset = 'Running Dinner dataset 2023 v2.xlsx'
oplossing1 = 'Running Dinner eerste oplossing 2023 v2.xlsx'

bewoners = pd.read_excel(dataset,sheet_name='Bewoners')
adressen = pd.read_excel(dataset,sheet_name='Adressen')
paar = pd.read_excel(dataset,sheet_name='Paar blijft bij elkaar',header = 1)
buren = pd.read_excel(dataset,sheet_name='Buren',header = 1)
kookte = pd.read_excel(dataset,sheet_name='Kookte vorig jaar',header = 1)
tafelgenoot = pd.read_excel(dataset,sheet_name='Tafelgenoot vorig jaar',header = 1)

oplossing = pd.read_excel(oplossing1)

df1 = oplossing

import random


def switch_addresses(df, df_paar, gangen=["Voor", "Hoofd", "Na"]):
    
    # Willekeurig een gang selecteren
    random_gang = random.choice(gangen)

    # Identificeer de indices van de bewoners die tijdens deze gang koken
    kokers_indices = df[df["kookt"] == random_gang].index.tolist()
    niet_kokers_indices = df.index.difference(kokers_indices).tolist()

    # Een willekeurige index selecteren die niet kookt voor deze gang
    bewoner1_index = random.choice(niet_kokers_indices)
    bewoner1 = df.loc[bewoner1_index, "Bewoner"]

    # Check of bewoner1 een paar heeft
    bewoner2 = None
    if bewoner1 in df_paar['Bewoner1'].values:
        bewoner2 = df_paar[df_paar['Bewoner1'] == bewoner1]['Bewoner2'].values[0]
    elif bewoner1 in df_paar['Bewoner2'].values:
        bewoner2 = df_paar[df_paar['Bewoner2'] == bewoner1]['Bewoner1'].values[0]

    # Als bewoner1 een paar heeft
    if bewoner2:
        bewoner2_index = df[df["Bewoner"] == bewoner2].index[0]
        adresA = df.loc[bewoner1_index, random_gang]

        # Selecteer een random adres B, maar niet adresA
        all_adresses = df[random_gang].unique().tolist()
        all_adresses.remove(adresA)
        adresB = random.choice(all_adresses)

        # Haal twee willekeurige indices op voor dit adres
        bewoners_met_adresB_indices = df[df[random_gang] == adresB].index.tolist()
        random.shuffle(bewoners_met_adresB_indices)
        bewoner3_index, bewoner4_index = bewoners_met_adresB_indices[:2]

        # Wissel de adressen
        df.loc[bewoner1_index, random_gang] = adresB
        df.loc[bewoner2_index, random_gang] = adresB
        df.loc[bewoner3_index, random_gang] = adresA
        df.loc[bewoner4_index, random_gang] = adresA

    # Als bewoner1 geen paar heeft, doe een eenvoudige adreswisseling
    else:
        available_indices = df.index.difference(kokers_indices).difference([bewoner1_index]).tolist()
        bewoner2_index = random.choice(available_indices)
        adres2 = df.loc[bewoner2_index, random_gang]

        df.loc[bewoner1_index, random_gang] = adres2
        df.loc[bewoner2_index, random_gang] = bewoner1

    return df


test1 = switch_addresses(df1,paar)
print(test1)
print(test1.loc[119])
print(test1.loc[120])