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

testje = new_state_pair(df1,paar)
print(testje)
