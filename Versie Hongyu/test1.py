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
df1 = oplossing.head(40)

#Wens1?
def calculate_repeated_meetings(df):
    #Wens 1
    deelnemers_adressen = {}
    
    # 1. Creëer een dictionary met de adressen voor elke deelnemer
    for _, row in df.iterrows():
        deelnemers_adressen[row['Bewoner']] = [row['Voor'], row['Hoofd'], row['Na']]
        
    # 2. Vergelijk de lijsten om te zien hoe vaak deelnemers dezelfde adressen hebben
    repeated_meetings = 0
    deelnemers = list(deelnemers_adressen.keys())

    for i in range(len(deelnemers)):
        for j in range(i+1, len(deelnemers)):
            # Tel hoeveel adressen de twee deelnemers gemeen hebben
            common_adressen = len(set(deelnemers_adressen[deelnemers[i]]) & set(deelnemers_adressen[deelnemers[j]]))
            if common_adressen > 1:
                # Als ze op meer dan 1 adres gemeenschappelijk hebben, tel het
                repeated_meetings += common_adressen - 1

    return repeated_meetings

#Simulated Annealing verwisselen met constraint 3
def new_state(df):
    """Creëert een nieuwe staat door twee willekeurige adressen van plaats te wisselen binnen een willekeurige kolom."""
    new_df = df.copy()
    
    # Kies een willekeurige kolom
    random_gang = np.random.choice(['Voor', 'Hoofd', 'Na'])
    # print(random_gang)
    
    # Kies twee willekeurige adressen uit de geselecteerde kolom
    valid_adressen = new_df[(new_df[random_gang] != new_df['Huisadres']) & (new_df[random_gang] != new_df['kookt'])]
    # print(valid_adressen)
    index_adres1, index_adres2 = np.random.choice(valid_adressen.index, size=2, replace=False)
    # print(index_adres1,index_adres2)

    # Verwissel de adressen
    new_df.at[index_adres1, random_gang], new_df.at[index_adres2, random_gang] = df.at[index_adres2, random_gang], df.at[index_adres1, random_gang]
    
    return new_df


total_repeated = calculate_repeated_meetings(df1)
print(f"Totaal aantal herhaalde ontmoetingen: {total_repeated}")


# check waar ze verwisselt zijn, er staat nog een print in de functie
# print(df1 == new_state(df1))
