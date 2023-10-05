import pandas as pd
from collections import OrderedDict
from itertools import combinations
import numpy as np

Filepath_Oplossing = 'Running Dinner eerste oplossing 2023 v2.xlsx'
Filepath_Dataset = 'Running Dinner dataset 2023 v2.xlsx'

Oplossing = pd.read_excel(Filepath_Oplossing)
    
Bewoners = pd.read_excel(Filepath_Dataset, sheet_name = 'Bewoners')
Adressen = pd.read_excel(Filepath_Dataset, sheet_name = 'Adressen')
Paar = pd.read_excel(Filepath_Dataset, sheet_name = 'Paar blijft bij elkaar', header = 1)
Buren = pd.read_excel(Filepath_Dataset, sheet_name = 'Buren', header = 1)
Kookte = pd.read_excel(Filepath_Dataset, sheet_name = 'Kookte vorig jaar', header = 1)
Tafelgenoot = pd.read_excel(Filepath_Dataset, sheet_name = 'Tafelgenoot vorig jaar', header = 1) 

def Wensen2(Oplossing, Kookte, Adressen, Buren, Tafelgenoot):
    
    ## Wens 1
        
    Wens1 = 0
    deelnemers_adressen = {}
    
    # 1. Creëer een dictionary met de adressen voor elke deelnemer
    for _, row in Oplossing.iterrows():
        deelnemers_adressen[row['Bewoner']] = [row['Voor'], row['Hoofd'], row['Na']]
        
    # 2. Vergelijk de lijsten om te zien hoe vaak deelnemers dezelfde adressen hebben
    deelnemers = list(deelnemers_adressen.keys())

    for i in range(len(deelnemers)):
        for j in range(i+1, len(deelnemers)):
            # Tel hoeveel adressen de twee deelnemers gemeen hebben
            common_adressen = len(set(deelnemers_adressen[deelnemers[i]]) & set(deelnemers_adressen[deelnemers[j]]))
            if common_adressen > 1:
                # Als ze op meer dan 1 adres gemeenschappelijk hebben, tel het
                Wens1 += common_adressen - 1
    
    ## Wens 2
    
    df_koken_hetzelfde = Oplossing.merge(Kookte, left_on=['Huisadres', 'kookt'], right_on=['Huisadres', 'Gang'], how='inner')
    df_koken_hoofdgerecht = df_koken_hetzelfde[df_koken_hetzelfde['Gang'] == 'Hoofd']
    Wens2 = df_koken_hoofdgerecht['Huisadres'].nunique()
    
    ## Wens 3
    
    df_voorkeur = Adressen.dropna(subset=['Voorkeur gang'])
    df_voorkeur_hetzelfde = Oplossing.merge(df_voorkeur, left_on=['Huisadres', 'kookt'], right_on=['Huisadres', 'Voorkeur gang'], how='inner')
    Wens3 = len(df_voorkeur) - df_voorkeur_hetzelfde['Huisadres'].nunique()
    
    ## Wens 4
    
    Buren['VoorBewoner1'] = Buren['Bewoner1'].map(Oplossing.set_index('Bewoner')['Voor'])
    Buren['VoorBewoner2'] = Buren['Bewoner2'].map(Oplossing.set_index('Bewoner')['Voor'])
    Buren['VoorSamen'] = (Buren['VoorBewoner1'] == Buren['VoorBewoner2'])
    Buren['HoofdBewoner1'] = Buren['Bewoner1'].map(Oplossing.set_index('Bewoner')['Hoofd'])
    Buren['HoofdBewoner2'] = Buren['Bewoner2'].map(Oplossing.set_index('Bewoner')['Hoofd'])
    Buren['HoofdSamen'] = (Buren['HoofdBewoner1'] == Buren['HoofdBewoner2'])
    Buren['NaBewoner1'] = Buren['Bewoner1'].map(Oplossing.set_index('Bewoner')['Na'])
    Buren['NaBewoner2'] = Buren['Bewoner2'].map(Oplossing.set_index('Bewoner')['Na'])
    Buren['NaSamen'] = (Buren['NaBewoner1'] == Buren['NaBewoner2'])
    Wens4 = Buren['VoorSamen'].sum() + Buren['HoofdSamen'].sum() + Buren['NaSamen'].sum()
    
    ## Wens 5
    
    tafelgenoten_list = []
    
    # Stap 1: Bepaal de tafelgenoten van dit jaar
    for gang in ['Voor', 'Hoofd', 'Na']:
        groepen = Oplossing.groupby(gang)['Bewoner'].apply(list)
        for bewoners in groepen:
            tafelgenoten_list.extend([(bewoner, genoot) for bewoner in bewoners for genoot in bewoners if bewoner != genoot])
    
    tafelgenoten_df = pd.DataFrame(tafelgenoten_list, columns=['Bewoner1', 'Bewoner2'])
    
    # Stap 2: Vergelijk de resultaten met tafelgenoot
    merged_df = pd.merge(tafelgenoten_df, Tafelgenoot, how='inner', left_on=['Bewoner1', 'Bewoner2'], right_on=['Bewoner1', 'Bewoner2'])
    Wens5 = len(merged_df)
    
    ## Kwaliteit oplossing
    
    Niveau = Wens1 + Wens2 + Wens3 + Wens4 + Wens5
    
    return Niveau, Wens1, Wens2, Wens3, Wens4, Wens5

Niveau, Wens1, Wens2, Wens3, Wens4, Wens5 = Wensen2(Oplossing, Kookte, Adressen, Buren, Tafelgenoot)
print(Niveau, Wens1, Wens2, Wens3, Wens4, Wens5)

