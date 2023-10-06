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

def toegelaten_indices(df, df_paar, gangen=["Voor", "Hoofd", "Na"]):
    random_gang = random.choice(gangen)

    kokers_indices = df[df["kookt"] == random_gang].index.tolist()
    
    # Maak een lijst van alle bewoners in de paren
    bewoners_in_paren = df_paar['Bewoner1'].tolist() + df_paar['Bewoner2'].tolist()

    # Index van de paren uit df_paar
    indices_in_paren = df[df['Bewoner'].isin(bewoners_in_paren)].index.tolist()
    
    index = list(set(df.index) - set(kokers_indices) - set(indices_in_paren))


    
    return index

# print(toegelaten_indices(df1,paar,gangen="Hoofd"))

def find_pair_indices(df, df_paar):
    resultaat = {}
    for _, row in df_paar.iterrows():
        idx1 = df[df['Bewoner'] == row['Bewoner1']].index.tolist()
        idx2 = df[df['Bewoner'] == row['Bewoner2']].index.tolist()
        if idx1 and idx2:  # als beide indices gevonden zijn
            pair_key = f"{row['Bewoner1']} & {row['Bewoner2']}"
            resultaat[pair_key] = (idx1[0], idx2[0])
    return resultaat

dict_paar = (find_pair_indices(df1,paar))
print(dict_paar)

# for paar in dict_paar:
#     deelnemer1 = dict_paar[paar][0]
#     deelnemer2 = dict_paar[paar][1]

def mogelijke_adressen(df, gang):
    # Filter de rijen waar de kookt kolom niet hetzelfde is als de gang
    gang_df = df[df["kookt"] != gang]
    
    # Tel de frequentie van elk adres onder de gegeven gang
    adres_telling = gang_df[gang].value_counts()
    
    # Filter adressen die minstens twee keer voorkomen
    geldige_adressen = adres_telling[adres_telling >= 2].index.tolist()
    
    return geldige_adressen

print(mogelijke_adressen(df1,'Hoofd',))

def ruil_adressen(df, paar_indices, gang, nieuw_adres):
    """
    Ruil de adressen van het paar met de adressen van de twee andere deelnemers die het 'nieuw_adres' hebben.
    """
    oud_adres_paar = df.loc[paar_indices[0], gang]

    # Zoek de indices van de deelnemers met het 'nieuw_adres' 
    def kies_twee_random_indices(df, gang, nieuw_adres, toegelaten_indices, max_pogingen=50):
        pogingen = 0
        
        while pogingen < max_pogingen:
            gefilterde_indices = df[(df[gang] == nieuw_adres) & (df["kookt"] != gang) & df.index.isin(toegelaten_indices)].index.tolist()

            # Als er ten minste 2 items in de lijst zijn
            if len(gefilterde_indices) >= 2:
                random_indices = random.sample(gefilterde_indices, 2)
                return random_indices
            
            pogingen += 1

        # Als we hier zijn, hebben we het maximale aantal pogingen bereikt zonder succes.
        print(f"Kon geen twee indices vinden na {max_pogingen} pogingen.")
        return None

    deelnemers_met_nieuw_adres = df[(df[gang] == nieuw_adres) & (df["kookt"] != gang)].index.tolist()
    
    # Wissel adressen
    df.loc[paar_indices, gang] = nieuw_adres
    df.loc[deelnemers_met_nieuw_adres, gang] = oud_adres_paar

    return df


def probeer_wisselingen(df, paar_idx):
    # Voor dit voorbeeld focussen we op de gang "Hoofd"
    gang = "Hoofd"
    
    huidig_adres = df.at[paar_idx[0], gang]
    
    # Krijg alle mogelijke adressen waar we mee kunnen ruilen
    adressen = mogelijke_adressen(df, gang)
    
    # Verwijder het huidige adres van het paar uit de lijst
    adressen.remove(huidig_adres)
    
    # for adres in adressen:
    #     # Maak een kopie van de oorspronkelijke dataframe
    #     df_kopie = df.copy()
        
    #     # Probeer het adres te wisselen
    #     df_kopie = wissel_adres_voor_paar(df_kopie, paar_idx, gang, adres)
        
    #     # Hier kunt u een functie oproepen om de "geschiktheid" of "wenselijkheid" van deze wisseling te controleren
    #     # bijvoorbeeld: if is_geschikt(df_kopie): ...

    # return df_kopie
