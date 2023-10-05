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

df1 = oplossing.head(20)

import random

def switch_addresses(df, df_paar, gangen=["Voor", "Hoofd", "Na"]):
    
    # Willekeurig een gang selecteren
    random_gang = random.choice(gangen)
    print(f"Geselecteerde gang: {random_gang}")
    
   # Identificeer de indices van de bewoners die tijdens deze gang koken
    kokers_indices = df[df["kookt"] == random_gang].index
    print(f"Indices van bewoners die koken tijdens {random_gang}: {kokers_indices}")

    # Gebruik de indices om de uitgesloten adressen te verkrijgen
    excluded_addresses = df.loc[kokers_indices, random_gang].tolist()
    print(f"Uitgesloten adressen (vanwege kokers): {excluded_addresses}")

    # Selecteer een willekeurige bewoner die niet kookt voor deze gang
    bewoner1_index = df[~df.index.isin(kokers_indices) & df[random_gang].notna()].sample().index[0]
    bewoner1 = df["Bewoner"][bewoner1_index]
    adres1 = df.loc[bewoner1_index, random_gang]

    print(f"Geselecteerde bewoner1 (niet kokend): {bewoner1} met adres: {adres1}")
    print(bewoner1_index)
    
    # Check of bewoner1 een paar heeft
    bewoner2 = None
    print(bewoner2)

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
        # Stap 1: Filter waar adres niet gelijk is aan adres1
        filtered_df = df[df[random_gang] != adres1]
        print('1',filtered_df)
        # Stap 2: Filter waar adres niet in excluded_addresses staat
        filtered_df = filtered_df[~filtered_df[random_gang].isin(excluded_addresses)]
        print('2',filtered_df)
        # Stap 3: Filter waar het adres niet leeg is
        filtered_df = filtered_df[filtered_df[random_gang].notna()]
        print('3',filtered_df)
        # Stap 4: Kies willekeurig één rij uit de gefilterde DataFrame
        random_row = filtered_df.sample()
        print(random_row)
        # Stap 5: Haal de index op van deze willekeurig gekozen rij
        bewoner2_index = random_row.index[0]

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