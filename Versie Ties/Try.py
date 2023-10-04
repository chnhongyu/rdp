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
    data = {}
    for index, row in Oplossing.iterrows():
        bewoner = row['Bewoner']
        voor = row['Voor']
        hoofd = row['Hoofd']
        na = row['Na']
        data[bewoner] = [voor, hoofd, na]

    # Maak een lege dictionary om de resultaten op te slaan
    resultaat_dict = {}

    # Genereer alle combinaties van 2 adressen
    adressen_combinaties = combinations(set(address for adreslijst in data.values() for address in adreslijst), 2)
    
    # Itereer over de combinaties en tel hoe vaak elk adrespaar voorkomt
    adrespaar_frequentie = {}
    for adres1, adres2 in adressen_combinaties:
        adrespaar_frequentie[(adres1, adres2)] = sum(1 for adreslijst in data.values() if adres1 in adreslijst and adres2 in adreslijst)
    
    # Controleer of er minimaal 2 bewoners zijn met hetzelfde adrespaar
    for adrespaar, frequentie in adrespaar_frequentie.items():
        if frequentie >= 2:
            bewoners_met_adrespaar = [bewoner for bewoner, adressen in data.items() if set(adrespaar).issubset(adressen)]
            resultaat_dict[adrespaar] = bewoners_met_adrespaar

    # Loop door de sleutels en tel de lengte van de bijbehorende lijst (waarden)
    for sleutel in resultaat_dict:
        Wens1 += len(resultaat_dict[sleutel])
    
    
    overeenkomende_gangen_teller = 0

    # Loop door elke rij in de dataset
    count = 0
    for index, row in Oplossing.iterrows():
        bewoner1 = row['Bewoner']
        gangen1 = np.array([row['Voor'], row['Hoofd'], row['Na']])
        
        # Loop door de overige rijen in de dataset
        for _, other_row in Oplossing.iloc[index+1:].iterrows():
            bewoner2 = other_row['Bewoner']
            gangen2 = np.array([other_row['Voor'], other_row['Hoofd'], other_row['Na']])
        
            
            # Als er minstens 2 overeenkomende gangen zijn, verhoog dan de teller
            # if len(overeenkomende_gangen) >= 2:
            #     overeenkomende_gangen_teller += 1

    # Print het totale aantal keren dat aan de voorwaarde is voldaan
    print("Aantal keren dat 2 verschillende bewoners minstens 2 dezelfde gangen hebben:", overeenkomende_gangen_teller)
    
    
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
    
    Tafelgenoot['VoorBewoner1'] = Tafelgenoot['Bewoner1'].map(Oplossing.set_index('Bewoner')['Voor'])
    Tafelgenoot['VoorBewoner2'] = Tafelgenoot['Bewoner2'].map(Oplossing.set_index('Bewoner')['Voor'])
    Tafelgenoot['VoorSamen'] = (Tafelgenoot['VoorBewoner1'] == Tafelgenoot['VoorBewoner2'])
    Tafelgenoot['HoofdBewoner1'] = Tafelgenoot['Bewoner1'].map(Oplossing.set_index('Bewoner')['Hoofd'])
    Tafelgenoot['HoofdBewoner2'] = Tafelgenoot['Bewoner2'].map(Oplossing.set_index('Bewoner')['Hoofd'])
    Tafelgenoot['HoofdSamen'] = (Tafelgenoot['HoofdBewoner1'] == Tafelgenoot['HoofdBewoner2'])
    Tafelgenoot['NaBewoner1'] = Tafelgenoot['Bewoner1'].map(Oplossing.set_index('Bewoner')['Na'])
    Tafelgenoot['NaBewoner2'] = Tafelgenoot['Bewoner2'].map(Oplossing.set_index('Bewoner')['Na'])
    Tafelgenoot['NaSamen'] = (Tafelgenoot['HoofdBewoner1'] == Tafelgenoot['HoofdBewoner2'])
    Wens5 = Tafelgenoot['VoorSamen'].sum() + Tafelgenoot['HoofdSamen'].sum() + Tafelgenoot['NaSamen'].sum()
    
    ## Kwaliteit oplossing
    
    Niveau = Wens1 + Wens2 + Wens3 + Wens4 + Wens5
    
    return Niveau, Wens1, Wens2, Wens3, Wens4, Wens5

Niveau, Wens1, Wens2, Wens3, Wens4, Wens5 = Wensen2(Oplossing, Kookte, Adressen, Buren, Tafelgenoot)
print(Niveau, Wens1, Wens2, Wens3, Wens4, Wens5)

