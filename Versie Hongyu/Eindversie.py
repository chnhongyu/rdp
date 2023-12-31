import pandas as pd
import numpy as np
import random
import math

# Inlezen dataset en feasible solution
dataset = 'Running Dinner dataset 2023 v2.xlsx'
oplossing1 = 'Running Dinner eerste oplossing 2023 v2.xlsx'

# DFs van dataset
bewoners = pd.read_excel(dataset,sheet_name='Bewoners')
adressen = pd.read_excel(dataset,sheet_name='Adressen')
paar = pd.read_excel(dataset,sheet_name='Paar blijft bij elkaar',header = 1)
buren = pd.read_excel(dataset,sheet_name='Buren',header = 1)
kookte = pd.read_excel(dataset,sheet_name='Kookte vorig jaar',header = 1)
tafelgenoot = pd.read_excel(dataset,sheet_name='Tafelgenoot vorig jaar',header = 1)
# Feasible solution
oplossing = pd.read_excel(oplossing1)

# df staat voor df_oplossing!
df = oplossing

# functie voor adressen wisselen (SA)
# Inclusief constraint 3 en 5. omdat deze wisseling allen 3 en 5 veranderd in feasiblity

def switch_addresses(df, df_paar, gangen=["Voor", "Hoofd", "Na"]):
    random_gang = random.choice(gangen)
    # print(f"Geselecteerde gang: {random_gang}")

    kokers_indices = df[df["kookt"] == random_gang].index.tolist()
    niet_kokers_indices = df.index.difference(kokers_indices).tolist()

    bewoner1_index = random.choice(niet_kokers_indices)
    bewoner1 = df.loc[bewoner1_index, "Bewoner"]

    bewoner2 = None
    if bewoner1 in df_paar['Bewoner1'].values:
        bewoner2 = df_paar[df_paar['Bewoner1'] == bewoner1]['Bewoner2'].values[0]
    elif bewoner1 in df_paar['Bewoner2'].values:
        bewoner2 = df_paar[df_paar['Bewoner2'] == bewoner1]['Bewoner1'].values[0]

    if bewoner2:
        bewoner2_index = df[df["Bewoner"] == bewoner2].index[0]
        
        adresA = df.loc[bewoner1_index, random_gang]
        
        unieke_adressen = df[random_gang].unique().tolist()
        unieke_adressen.remove(adresA)  # Verwijder adresA uit de selecteerbare adressen

        adresB = random.choice(unieke_adressen)
        bewoners_met_adresB_indices = df[df[random_gang] == adresB].index.tolist()

        while len(bewoners_met_adresB_indices) < 2:
            unieke_adressen.remove(adresB)
            if not unieke_adressen:
                print("Kan geen geldig adres vinden met minimaal 2 bewoners.")
                return df
            adresB = random.choice(unieke_adressen)
            bewoners_met_adresB_indices = df[df[random_gang] == adresB].index.tolist()

        random.shuffle(bewoners_met_adresB_indices)
        bewoner3_index, bewoner4_index = bewoners_met_adresB_indices[:2]

        # Debug-prints
        # print(f"Paar gevonden: {bewoner1} en {bewoner2}")
        # print(f"Adressen vóór wisseling: {bewoner1}: {adresA}, {bewoner2}: {adresA}")
        # print(f"Wisselend met paar: {df.loc[bewoner3_index, 'Bewoner']} en {df.loc[bewoner4_index, 'Bewoner']}")
        # print(f"Adressen vóór wisseling: {df.loc[bewoner3_index, 'Bewoner']}: {adresB}, {df.loc[bewoner4_index, 'Bewoner']}: {adresB}")

        # Adressen wisselen
        df.loc[bewoner1_index, random_gang] = adresB
        df.loc[bewoner2_index, random_gang] = adresB
        df.loc[bewoner3_index, random_gang] = adresA
        df.loc[bewoner4_index, random_gang] = adresA

        # Debug-prints na wisseling
        # print(f"Adressen na wisseling: {bewoner1}: {df.loc[bewoner1_index, random_gang]}, {bewoner2}: {df.loc[bewoner2_index, random_gang]}, {df.loc[bewoner3_index, 'Bewoner']}: {df.loc[bewoner3_index, random_gang]}, {df.loc[bewoner4_index, 'Bewoner']}: {df.loc[bewoner4_index, random_gang]}")

    else:
        available_indices = df.index.difference(kokers_indices).difference([bewoner1_index]).tolist()
        bewoner2_index = random.choice(available_indices)
        adres2 = df.loc[bewoner2_index, random_gang]
        df.loc[bewoner1_index, random_gang] = adres2
        df.loc[bewoner2_index, random_gang] = bewoner1

    return df



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


#Wens3


#Wens4


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
def Wens(df, tafelgenoot):
    resultaat_wens1 = Wens1(df)
    resultaat_wens5 = Wens5(df, tafelgenoot)

    totaal = resultaat_wens1 + resultaat_wens5
    return totaal

#-----------------------------
#Constraint Check
def Constraints(Dataset, df_oplossing):
    
    ## Inlezen van dataset en oplossing
    
    Bewoners = pd.read_excel(Dataset, sheet_name = 'Bewoners')
    Adressen = pd.read_excel(Dataset, sheet_name = 'Adressen')
    Paar = pd.read_excel(Dataset, sheet_name = 'Paar blijft bij elkaar', header = 1)
    Buren = pd.read_excel(Dataset, sheet_name = 'Buren', header = 1)
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
        lb = Adressen[ Adressen['Huisadres']== a ]['Min groepsgrootte'].values
        ub = Adressen[ Adressen['Huisadres']== a ]['Max groepsgrootte'].values
        if adres_count[a]>ub or adres_count[a]<lb:
            print('Er wordt niet voldaan aan Constraint 4')
    
    ## Constraint 5

    for paar,(d1,d2) in Paar.iterrows():
        lhs = df_oplossing[ df_oplossing['Bewoner']==d1 ][ ['Voor','Hoofd','Na'] ].values.tolist()
        rhs = df_oplossing[ df_oplossing['Bewoner']==d2 ][ ['Voor','Hoofd','Na'] ].values.tolist()
        if lhs != rhs:
            print('Er wordt niet voldaan aan Constraint 5')
        continue 

#-----------------------------

def simulated_annealing(df, df_paar, max_iterations=1000, start_temp=1000, alpha=0.995):
    current_df = df.copy()
    current_cost = Wens(current_df, df_paar)  # Aangenomen dat je Wens functie het totale aantal wensen retourneert dat niet wordt voldaan.
    
    best_df = current_df.copy()
    best_cost = current_cost

    temp = start_temp

    for iteration in range(max_iterations):
        new_df = switch_addresses(current_df, df_paar)
        new_cost = Wens(new_df, df_paar)
        
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

result_df, result_cost = simulated_annealing(df,paar)


print(result_cost)
print(Constraints(dataset,result_df))
