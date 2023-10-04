import pandas as pd
import numpy as np

dataset = 'Running Dinner dataset 2023 v2.xlsx'

oplossing1 = 'Running Dinner eerste oplossing 2023 v2.xlsx'
# oplossing2 = 'Running Dinner tweede oplossing 2023 v2.xlsx'
# oplossing2022 = 'Running Dinner eerste oplossing 2022.xlsx'


bewoners = pd.read_excel(dataset,sheet_name='Bewoners')
adressen = pd.read_excel(dataset,sheet_name='Adressen')
paar = pd.read_excel(dataset,sheet_name='Paar blijft bij elkaar',header = 1)
buren = pd.read_excel(dataset,sheet_name='Buren',header = 1)
kookte = pd.read_excel(dataset,sheet_name='Kookte vorig jaar',header = 1)
tafelgenoot = pd.read_excel(dataset,sheet_name='Tafelgenoot vorig jaar',header = 1)

oplossing = pd.read_excel(oplossing1)
df1 = oplossing

#Wens1 check
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

#Wens1:
total_repeated = calculate_repeated_meetings(df1)
print(f"Totaal aantal herhaalde ontmoetingen: {total_repeated}")


# #Wens2 fout
# def herhaling_hoofdgerecht(df1, kookte):
#     # Filter de adressen uit de 'kookte' dataframe die vorig jaar 'Hoofd' hebben gekookt
#     vorig_jaar_hoofd = kookte[kookte['Gang'] == 'Hoofd']['Huisadres']
    
#     # Check in de 'df1' dataframe welke van deze adressen dit jaar opnieuw 'Hoofd' koken
#     dit_jaar_hoofd = df1[(df1['Huisadres'].isin(vorig_jaar_hoofd)) & (df1['kookt'] == 'Hoofd')]

#     return len(dit_jaar_hoofd)

# #Wens3 fout
# def count_unsatisfied_preferences(df1, adressen):
#     # Filter adressen met een voorkeur
#     voorkeur_adressen = adressen.dropna(subset=['Voorkeur gang'])

#     # Merge de dataframes op 'Huisadres'
#     merged_df = pd.merge(voorkeur_adressen, df1[['Huisadres', 'kookt']], on='Huisadres', how='inner')

#     # Voeg een boolean kolom toe die aangeeft of de voorkeur wordt voldaan
#     merged_df['voorkeur_voldaan'] = merged_df['Voorkeur gang'] == merged_df['kookt']

#     # Tel de aantal False waarden in de 'voorkeur_voldaan' kolom
#     unsatisfied_count = (~merged_df['voorkeur_voldaan']).sum()

#     return unsatisfied_count



# aantal_herhalingen = herhaling_hoofdgerecht(df1, kookte)
# print(f"Aantal adressen die zowel vorig jaar als dit jaar een hoofdgerecht koken: {aantal_herhalingen}")

# niet_voldaan = count_unsatisfied_preferences(df1, adressen)
# print(f"Aantal adressen waarvan de voorkeur niet is voldaan: {niet_voldaan}")



#Simulated Annealing verwisselen met constraint 3 en 5
def new_state_pair(df1, paar):
    df_new = df1.copy()
    
    # Kies willekeurig een kolom (VOOR, HOOFD, NA).
    random_gang = np.random.choice(['Voor', 'Hoofd', 'Na'])
    print(f'gang = {random_gang}')

    # Kies een willekeurig adres uit die kolom.
    adres1 = np.random.choice(df1[random_gang])
    
    # Vind de index van het gekozen adres
    index_adres1 = df1[df1[random_gang] == adres1].index[0]
    print(f'adres = {adres1}, index = {index_adres1}')


    # Vind de bewoner die op dat adres zal zijn voor de gekozen maaltijd.
    bewoner1 = df_new[df_new[random_gang] == adres1]['Bewoner'].iloc[0]
    print(f'bewoner= {bewoner1}')

    # Controleer of de bewoner deel uitmaakt van een paar.
    is_pair = paar[(paar['Bewoner1'] == bewoner1) | (paar['Bewoner2'] == bewoner1)]
    print(is_pair)
    print(not is_pair.empty)

    if not is_pair.empty:  # Als bewoner deel uitmaakt van een paar.
        bewoner2 = is_pair['Bewoner2'].iloc[0] if is_pair['Bewoner1'].iloc[0] == bewoner1 else is_pair['Bewoner1'].iloc[0]
        adres2 = df_new[df_new['Bewoner'] == bewoner2][random_gang].iloc[0]
        
        # Filter adressen waar geen constraint wordt overtreden.
        available = df1[(df1[random_gang] != adres1) & 
                       (df1[random_gang] != adres2) & 
                       (df1['Bewoner'] != bewoner1) & 
                       (df1['Bewoner'] != bewoner2) & 
                       (df1[random_gang] != df1['kookt']) & 
                       (df1[random_gang] != df1['Huisadres'])]
        
        if not available.empty:
            adres2 = np.random.choice(available['Huisadres'])
            df_new.loc[df_new[random_gang] == adres1, random_gang] = adres2
            df_new.loc[df_new[random_gang] == adres2, random_gang] = adres2
            df_new.loc[df_new['Huisadres'] == adres2, random_gang] = adres1
    else:  # Als het een normale bewoner is.
        available = df1[(df1[random_gang] != adres1) & 
                       (df1['Bewoner'] != bewoner1) & 
                       (df1[random_gang] != df1['kookt']) & 
                       (df1[random_gang] != df1['Huisadres'])]
        
        if not available.empty:
            adres2 = np.random.choice(available['Huisadres'])
            df_new.loc[df_new[random_gang] == adres1, random_gang] = adres2
            df_new.loc[df_new['Huisadres'] == adres2, random_gang] = adres1
    print(adres2)
    return df_new



