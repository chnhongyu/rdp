import pandas as pd
import numpy as np
import random
import math

# Inlezen dataset en feasible solution
dataset = 'Running Dinner dataset 2023 v2.xlsx'
oplossing1 = 'Running Dinner eerste oplossing 2023 v2.xlsx'

bewoners = pd.read_excel(dataset,sheet_name='Bewoners')
adressen = pd.read_excel(dataset,sheet_name='Adressen')
paar = pd.read_excel(dataset,sheet_name='Paar blijft bij elkaar',header = 1)
buren = pd.read_excel(dataset,sheet_name='Buren',header = 1)
kookte = pd.read_excel(dataset,sheet_name='Kookte vorig jaar',header = 1)
tafelgenoot = pd.read_excel(dataset,sheet_name='Tafelgenoot vorig jaar',header = 1)

# Feasible solution
df = pd.read_excel(oplossing1)

# functie voor adressen wisselen (SA)
def switch_addresses(df, df_paar, gangen=["Voor", "Hoofd", "Na"]):
    random_gang = random.choice(gangen)

    kokers_indices = df[df["kookt"] == random_gang].index.tolist()
    
    # Maak een lijst van alle bewoners in de paren
    bewoners_in_paren = df_paar['Bewoner1'].tolist() + df_paar['Bewoner2'].tolist()
    
    # Verkrijg indices van bewoners in paren
    indices_in_paren = df[df['Bewoner'].isin(bewoners_in_paren)].index.tolist()

    # Verwijder indices van bewoners die in een paar zitten en die koken
    niet_kokers_indices = list(set(df.index) - set(kokers_indices) - set(indices_in_paren))

    if not niet_kokers_indices:
        print("Er zijn geen beschikbare niet-kokers die niet in een paar zitten.")
        return df

    bewoner1_index = random.choice(niet_kokers_indices)
    bewoner1 = df.loc[bewoner1_index, "Bewoner"]

    # Debug: print geselecteerde bewoner1
    # print("Geselecteerde bewoner1:", bewoner1)

    beschikbare_indices = list(set(df.index) - set(kokers_indices) - set([bewoner1_index]) - set(indices_in_paren))
    
    if not beschikbare_indices:
        print("Er zijn geen andere beschikbare niet-kokers om mee te wisselen.")
        return df

    bewoner2_index = random.choice(beschikbare_indices)
    bewoner2 = df.loc[bewoner2_index, "Bewoner"]

    # Debug: print geselecteerde bewoner2
    # print("Geselecteerde bewoner2:", bewoner2)

    adres1 = df.loc[bewoner1_index, random_gang]
    adres2 = df.loc[bewoner2_index, random_gang]
    df.loc[bewoner1_index, random_gang] = adres2
    df.loc[bewoner2_index, random_gang] = adres1

    return df


# wens functies rekent alleen over df en returnt een cijfer
#------------------------------
#Wens1
def Wens1(df):
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

#Wens2
def Wens2(df,kookte):
    df_koken_hetzelfde = df.merge(kookte, left_on=['Huisadres', 'kookt'], right_on=['Huisadres', 'Gang'], how='inner')
    df_koken_hoofdgerecht = df_koken_hetzelfde[df_koken_hetzelfde['Gang'] == 'Hoofd']
    wens2 = df_koken_hoofdgerecht['Huisadres'].nunique()
    return wens2
    
## Wens 3
def Wens3(df,adressen):
    df_voorkeur = adressen.dropna(subset=['Voorkeur gang'])
    df_voorkeur_hetzelfde = df.merge(df_voorkeur, left_on=['Huisadres', 'kookt'], right_on=['Huisadres', 'Voorkeur gang'], how='inner')
    wens3 = len(df_voorkeur) - df_voorkeur_hetzelfde['Huisadres'].nunique()
    return wens3
    
## Wens 4
def Wens4(df,buren):
    buren['VoorBewoner1'] = buren['Bewoner1'].map(df.set_index('Bewoner')['Voor'])
    buren['VoorBewoner2'] = buren['Bewoner2'].map(df.set_index('Bewoner')['Voor'])
    buren['VoorSamen'] = (buren['VoorBewoner1'] == buren['VoorBewoner2'])
    buren['HoofdBewoner1'] = buren['Bewoner1'].map(df.set_index('Bewoner')['Hoofd'])
    buren['HoofdBewoner2'] = buren['Bewoner2'].map(df.set_index('Bewoner')['Hoofd'])
    buren['HoofdSamen'] = (buren['HoofdBewoner1'] == buren['HoofdBewoner2'])
    buren['NaBewoner1'] = buren['Bewoner1'].map(df.set_index('Bewoner')['Na'])
    buren['NaBewoner2'] = buren['Bewoner2'].map(df.set_index('Bewoner')['Na'])
    buren['NaSamen'] = (buren['NaBewoner1'] == buren['NaBewoner2'])
    wens4 = buren['VoorSamen'].sum() + buren['HoofdSamen'].sum() + buren['NaSamen'].sum()
    return wens4

#Wens5
def Wens5(df1, tafelgenoot):
    # Stap 1: Bepaal de tafelgenoten van dit jaar
    def find_tafelgenoten(gang):
        groepen = df1.groupby(gang)['Bewoner'].apply(list)
        tafelgenoten = []
        for bewoners in groepen:
            tafelgenoten.extend([(bewoner, genoot) for bewoner in bewoners for genoot in bewoners if bewoner != genoot])
        return tafelgenoten

    tafelgenoten_list = sum([find_tafelgenoten(gang) for gang in ['Voor', 'Hoofd', 'Na']], [])
    tafelgenoten_df = pd.DataFrame(tafelgenoten_list, columns=['Bewoner1', 'Bewoner2'])
    
    # Stap 2: Vergelijk de resultaten met tafelgenoot
    merged_df = pd.merge(tafelgenoten_df, tafelgenoot, how='inner', left_on=['Bewoner1', 'Bewoner2'], right_on=['Bewoner1', 'Bewoner2'])
    return len(merged_df)

#-----------------------------
#Wensen bijelkaar
def Wens(df,kookte,adressen,buren,tafelgenoot):
    resultaat_wens1 = 2* Wens1(df)
    resultaat_wens2 = 10* Wens2(df,kookte)
    resultaat_wens3 = 10* Wens3(df,adressen)
    resultaat_wens4 = 3* Wens4(df,buren)
    resultaat_wens5 = Wens5(df,tafelgenoot)
    
    totaal = resultaat_wens1 + resultaat_wens2 + resultaat_wens3 + resultaat_wens4 + resultaat_wens5
    totaal = totaal

    return totaal

#-----------------------------
#Constraint Check
def Constraints(Dataset, df_oplossing):
    
    ## Inlezen van dataset en oplossing
    
    Bewoners = pd.read_excel(Dataset, sheet_name = 'Bewoners')
    adressen = pd.read_excel(Dataset, sheet_name = 'Adressen')
    Paar = pd.read_excel(Dataset, sheet_name = 'Paar blijft bij elkaar', header = 1)
    buren = pd.read_excel(Dataset, sheet_name = 'Buren', header = 1)
    Kookte = pd.read_excel(Dataset, sheet_name = 'Kookte vorig jaar', header = 1)
    Tafelgenoot = pd.read_excel(Dataset, sheet_name = 'Tafelgenoot vorig jaar', header = 1)    
    
    ## Constraint 1
    
    Deelnemer_ongelijk_aan_3 = {}
    for deelnemer in df_oplossing['Bewoner']:
        gangen = df_oplossing[df_oplossing['Bewoner']==deelnemer][['Voor','Hoofd','Na']].values[0]
        aantal_gangen = len(set(gangen))
        if aantal_gangen !=3:
            Deelnemer_ongelijk_aan_3[deelnemer] = aantal_gangen
    if len(Deelnemer_ongelijk_aan_3) > 0:
        print('Er wordt niet voldaan aan Constraint 1')
        
    ## Constraint 2
    
    set_adres = set(df_oplossing['Huisadres'])
    for adres in set_adres:
        if ( len( set( df_oplossing[ df_oplossing['Huisadres']==adres ]['kookt'].values ) )) != 1:
            print('Er wordt niet voldaan aan Constraint 2')

    ## Constraint 3
    
    Checklijst = []
    df_kokend = df_oplossing.dropna(subset=['kookt'])
    for deelnemer in range(len(df_kokend)):
        gang = df_kokend.iloc[deelnemer]['kookt']
        lhs = df_kokend.iloc[deelnemer][gang]
        rhs = df_kokend.iloc[deelnemer]['Huisadres']
        if lhs != rhs:
            Checklijst.append(df_kokend.iloc[deelnemer]['Bewoner'])
    if len(Checklijst) > 0:
        print('Er wordt niet voldaan aan Constraint 3') 
        
    ## Constraint 4
    
    kokend = df_oplossing.dropna(subset=['kookt'])
    adres_count = {}
    for index_bewoners, rij in kokend.iterrows():
        if rij['Huisadres'] not in adres_count:
            adres_count[rij['Huisadres']] = rij['aantal'] 
    for a in adres_count:
        lb = adressen[ adressen['Huisadres']== a ]['Min groepsgrootte'].values
        ub = adressen[ adressen['Huisadres']== a ]['Max groepsgrootte'].values
        if adres_count[a]>ub or adres_count[a]<lb:
            print('Er wordt niet voldaan aan Constraint 4')
    
    ## Constraint 5

    for paar,(d1,d2) in Paar.iterrows():
        lhs = df_oplossing[ df_oplossing['Bewoner']==d1 ][ ['Voor','Hoofd','Na'] ].values.tolist()
        rhs = df_oplossing[ df_oplossing['Bewoner']==d2 ][ ['Voor','Hoofd','Na'] ].values.tolist()
        if lhs != rhs:
            print('Er wordt niet voldaan aan Constraint 5')
        break

#-----------------------------

def simulated_annealing(df, dataset, max_iterations=5000, start_temp=100000, alpha=0.9995):
    current_df = df.copy()
    current_cost = Wens(current_df,kookte,adressen,buren,tafelgenoot)  # Aangenomen dat je Wens functie het totale aantal wensen retourneert dat niet wordt voldaan.
    
    best_df = current_df.copy()
    best_cost = current_cost

    temp = start_temp

    for iteration in range(max_iterations):
        new_df = switch_addresses(current_df, paar)
        new_cost = Wens(new_df,kookte,adressen,buren,tafelgenoot)
        
        cost_diff = new_cost - current_cost
        
        if cost_diff < 0 or random.uniform(0, 1) < math.exp(-cost_diff / temp):
            current_df = new_df
            current_cost = new_cost
            
            if current_cost < best_cost:
                best_df = current_df.copy()
                best_cost = current_cost
        
        temp *= alpha  # Vermindering van de temperatuur
        print(f'iteratie = {iteration}, cost = {best_cost}')
    
    return best_df, best_cost

result_df, result_cost = simulated_annealing(df,dataset)

print(result_cost,result_df)
print(Constraints(dataset,result_df))
print(Constraints(dataset,df))
