import pandas as pd
import numpy as np
import random 

# Data inladen
dataset = 'Running Dinner dataset 2023 v2.xlsx'
oplossing1 = 'Running Dinner eerste oplossing 2023 v2.xlsx'

bewoners = pd.read_excel(dataset,sheet_name='Bewoners')
adressen = pd.read_excel(dataset,sheet_name='Adressen')
paar = pd.read_excel(dataset,sheet_name='Paar blijft bij elkaar',header = 1)
buren = pd.read_excel(dataset,sheet_name='Buren',header = 1)
kookte = pd.read_excel(dataset,sheet_name='Kookte vorig jaar',header = 1)
tafelgenoot = pd.read_excel(dataset,sheet_name='Tafelgenoot vorig jaar',header = 1)
df = pd.read_excel(oplossing1)

def toegelaten_indices(df, df_paar):
    kokers_indices = df[df["kookt"] == random.choice(["Voor", "Hoofd", "Na"])].index.tolist()
    bewoners_in_paren = df_paar['Bewoner1'].tolist() + df_paar['Bewoner2'].tolist()
    indices_in_paren = df[df['Bewoner'].isin(bewoners_in_paren)].index.tolist()
    index = list(set(df.index) - set(kokers_indices) - set(indices_in_paren))
    print(f"Toegelaten indices: {index}")
    return index

def find_pair_indices(df, df_paar):
    resultaat = {}
    for _, row in df_paar.iterrows():
        idx1 = df[df['Bewoner'] == row['Bewoner1']].index.tolist()
        idx2 = df[df['Bewoner'] == row['Bewoner2']].index.tolist()
        if idx1 and idx2:
            pair_key = f"{row['Bewoner1']} & {row['Bewoner2']}"
            resultaat[pair_key] = (idx1[0], idx2[0])
    print(f"Pair indices: {resultaat}")
    return resultaat


def wissel_adres_voor_paar(df, paar_indices, gang, toegelaten_indices):
    if all(df.loc[paar_indices, 'kookt'] == gang):
        print("Paar kookt al voor deze gang.")
        return None
    huidig_adres = df.loc[paar_indices[0], gang]
    nieuw_adres_candidates = df.loc[toegelaten_indices, gang].unique().tolist()
    nieuw_adres_candidates.remove(huidig_adres)
    nieuw_adres = random.choice(nieuw_adres_candidates)
    def kies_twee_random_indices(df, gang, nieuw_adres, toegelaten_indices, max_pogingen=50):
        pogingen = 0
        while pogingen < max_pogingen:
            gefilterde_indices = df[(df[gang] == nieuw_adres) & (df["kookt"] != gang) & df.index.isin(toegelaten_indices)].index.tolist()
            if len(gefilterde_indices) >= 2:
                random_indices = random.sample(gefilterde_indices, 2)
                print(f"Gekozen indices: {random_indices}")
                return random_indices
            pogingen += 1
        print(f"Kon geen twee indices vinden na {max_pogingen} pogingen.")
        return None


    deelnemers_met_nieuw_adres = kies_twee_random_indices(df, gang, nieuw_adres, toegelaten_indices)
    if not deelnemers_met_nieuw_adres:
        return None
    df.loc[paar_indices, gang] = nieuw_adres
    df.loc[deelnemers_met_nieuw_adres, gang] = huidig_adres
    print(f"Adressen gewisseld voor paar {paar_indices} en deelnemers {deelnemers_met_nieuw_adres}.")
    return df

# Voorbeeld van uitvoering
toegelaten = toegelaten_indices(df, paar)
paar_index_map = find_pair_indices(df, paar)
een_paar = next(iter(paar_index_map.values()))
gang = "Hoofd"
wissel_adres_voor_paar(df, een_paar, gang, toegelaten)
