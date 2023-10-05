import pandas as pd
import numpy as np

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
    print(f"Geselecteerde gang: {random_gang}")
    
    # Identificeer de bewoners die tijdens deze gang koken
    kokers = df[df["kookt"] == random_gang]["Bewoner"].tolist()
    print(f"Bewoners die koken tijdens {random_gang}: {kokers}")
    
    # Hun adressen uitsluiten voor de wissel
    excluded_addresses = df[df["Bewoner"].isin(kokers)][random_gang].tolist()
    print(f"Uitgesloten adressen (vanwege kokers): {excluded_addresses}")
    
    # Een willekeurige bewoner selecteren die niet kookt voor deze gang
    bewoner1_index = df[(~df["Bewoner"].isin(kokers)) & (df[random_gang].notna())].sample().index[0]
    bewoner1 = df.loc[bewoner1_index, "Bewoner"]
    adres1 = df.loc[bewoner1_index, random_gang]
    print(f"Geselecteerde bewoner1 (niet kokend): {bewoner1} met adres: {adres1}")
    
    # Check of bewoner1 een paar heeft
    bewoner2 = None
    if bewoner1 in df_paar['Bewoner1'].values:
        bewoner2 = df_paar[df_paar['Bewoner1'] == bewoner1]['Bewoner2'].values[0]
    elif bewoner1 in df_paar['Bewoner2'].values:
        bewoner2 = df_paar[df_paar['Bewoner2'] == bewoner1]['Bewoner1'].values[0]
    
    # Als bewoner1 een paar heeft, beide adressen verzamelen
    if bewoner2:
        bewoner2_index = df[df["Bewoner"] == bewoner2].index[0]
        adres2 = df.loc[bewoner2_index, random_gang]
        print(f"Bewoner1 {bewoner1} heeft een paar: {bewoner2} met adres: {adres2}")
    else:
        # Een willekeurig ander adres selecteren voor de wissel, terwijl kokers worden uitgesloten
        bewoner2_index = df[(df[random_gang] != adres1) & (~df[random_gang].isin(excluded_addresses)) & (df[random_gang].notna())].sample().index[0]
        adres2 = df.loc[bewoner2_index, random_gang]
        print(f"Bewoner1 {bewoner1} heeft geen paar. Willekeurig geselecteerde bewoner2: {df.loc[bewoner2_index, 'Bewoner']} met adres: {adres2}")

    # Adressen wisselen
    df.loc[bewoner1_index, random_gang] = adres2
    df.loc[bewoner2_index, random_gang] = adres1
    print(f"Adres1 ({bewoner1}) is verwisseld naar: {adres2}")
    print(f"Adres2 ({df.loc[bewoner2_index, 'Bewoner']}) is verwisseld naar: {adres1}")

    return df

test1 = switch_addresses(df1,paar)
print(test1)