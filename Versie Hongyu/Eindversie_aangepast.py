# Importeren libraries 
import pandas as pd
import random
import math
import matplotlib.pyplot as plt

# Inlezen dataset en feasible solution
dataset = 'Running Dinner dataset 2023 v2.xlsx'
oplossing1 = 'Running Dinner eerste oplossing 2023 v2.xlsx'
oplossing2 = 'Running Dinner tweede oplossing 2023 v2.xlsx'

bewoners = pd.read_excel(dataset,sheet_name='Bewoners')
adressen = pd.read_excel(dataset,sheet_name='Adressen')
paar = pd.read_excel(dataset,sheet_name='Paar blijft bij elkaar',header = 1)
buren = pd.read_excel(dataset,sheet_name='Buren',header = 1)
kookte = pd.read_excel(dataset,sheet_name='Kookte vorig jaar',header = 1)
tafelgenoot = pd.read_excel(dataset,sheet_name='Tafelgenoot vorig jaar',header = 1)

# Feasible solution
df1 = pd.read_excel(oplossing1)
df2 = pd.read_excel(oplossing2)

# functie voor adressen wisselen (SA)
def switch_addresses(df, df_paar, gangen=["Voor", "Hoofd", "Na"]):
    ''' 
    Functie switch_addresses eist een input df voor feasible solution,
    df_paar is input uit de dataset om de paren te identificeren.

    Er wordt hier eerst een random gang geselecteerd uit "Voor" "Hoofd" "Na".
    Vervolgens worden er twee random bewoners geselecteerd en de 
    bijbehoorende adressen op die gang en deze worden omgewisseld.
    Er wordt rekening gehouden met welke gang de deelnemer voor gaat bereiden.
    Dit adres wordt niet geselecteerd om te wisselen, zodat constraint 3 niet wordt overschreden.

    Paar houden we hier buiten beschouwing vanwegen feasiblity. Zij worden niet verwisseld.
    '''
    random_gang = random.choice(gangen)

    niet_toegelaten_indices = df[df["kookt"] == random_gang].index.tolist()
    
    # Maak een lijst van alle bewoners in de paren
    bewoners_in_paren = df_paar['Bewoner1'].tolist() + df_paar['Bewoner2'].tolist()
    
    # Verkrijg indices van bewoners in paren
    paren_indices = df[df['Bewoner'].isin(bewoners_in_paren)].index.tolist()

    # Verwijder indices van bewoners die in een paar zitten en die koken
    toegelaten_indices = list(set(df.index) - set(niet_toegelaten_indices) - set(paren_indices))

    if not toegelaten_indices:
        print("Error; geen toegelaten oplossing")
        return df

    bewoner1_index = random.choice(toegelaten_indices)
    bewoner1 = df.loc[bewoner1_index, "Bewoner"]
    
    # Hier wordt bewoner1 uitgesloten
    beschikbare_indices = list(set(df.index) - set(niet_toegelaten_indices) - set([bewoner1_index]) - set(paren_indices))
    
    if not beschikbare_indices:
        print("Error; geen toegelaten oplossing")
        return df

    bewoner2_index = random.choice(beschikbare_indices)
    bewoner2 = df.loc[bewoner2_index, "Bewoner"]

    # Debug: print geselecteerde bewoner1 en 2
    # print("Geselecteerde bewoner1:", bewoner1)
    # print("Geselecteerde bewoner2:", bewoner2)

    adres1 = df.loc[bewoner1_index, random_gang]
    adres2 = df.loc[bewoner2_index, random_gang]
    df.loc[bewoner1_index, random_gang] = adres2
    df.loc[bewoner2_index, random_gang] = adres1

    return df

#------------------------------------------------------------------------------------
# Wens1 - Aantal herhalingen. Prioriteit 1
def Wens1(df):
    '''
    Wens1 eist als input df, een feasible solution.
    Wens1 gaat kijken hoevaak in de df, de wens is overschreden.
    Returnt een parameter.
    '''
    deelnemers_adressen = {}
    
    # Creëer een dictionary met de adressen voor elke deelnemer
    for _, rij in df.iterrows():
        deelnemers_adressen[rij['Bewoner']] = [rij['Voor'], rij['Hoofd'], rij['Na']]
        
    # Vergelijk de lijsten om te zien hoe vaak deelnemers dezelfde adressen hebben
    aantal_fouten = 0
    deelnemers = list(deelnemers_adressen.keys())

    for i in range(len(deelnemers)):
        for j in range(i+1, len(deelnemers)):
            
            # Tel hoeveel adressen de twee deelnemers gemeen hebben
            overeenkomende_adressen = len(set(deelnemers_adressen[deelnemers[i]]) & set(deelnemers_adressen[deelnemers[j]]))
            if overeenkomende_adressen > 1:
                
                # Als ze op meer dan 1 adres gemeenschappelijk eten, tel het op
                aantal_fouten += overeenkomende_adressen - 1

    return aantal_fouten

# Wens2 - Hoofdgerecht vorig jaar. Prioriteit 2
def Wens2(df,kookte):
    '''
    Wens2 eist als input df, een feasible solution en df_kookte uit de dataset.
    Wens2 gaat kijken hoevaak in de df, de wens is overschreden.
    Returnt een parameter.
    '''
    # Maak een dataframe waarbij wordt gekeken wie hetzelfde kookt als vorig jaar
    df_koken_hetzelfde = df.merge(kookte, left_on=['Huisadres', 'kookt'], right_on=['Huisadres', 'Gang'], how='inner')
    
    # Kijk of die gang 'Hoofd' is en zo ja tel hoe vaak dit voorkomt
    df_koken_hoofdgerecht = df_koken_hetzelfde[df_koken_hetzelfde['Gang'] == 'Hoofd']
    aantal_fouten = df_koken_hoofdgerecht['Huisadres'].nunique()
    return aantal_fouten
    
# Wens 3 - Adres krijgt zijn opgegeven voorkeur. Prioriteit 3
def Wens3(df,adressen):
    '''
    Wens3 eist als input df, een feasible solution en df_adressen uit de dataset.
    Wens3 gaat kijken hoevaak in de df, de wens is overschreden.
    Returnt een parameter.
    '''
    # Maak eerst een dataframe met alle huisadressen die een voorkeur voor een gang hebben
    df_voorkeur = adressen.dropna(subset=['Voorkeur gang'])
   
    # Vergelijk of deze voorkeuren overeenkomen, zo niet tel hoe vaak dit voorkomt.
    df_voorkeur_hetzelfde = df.merge(df_voorkeur, left_on=['Huisadres', 'kookt'], right_on=['Huisadres', 'Voorkeur gang'], how='inner')
    aantal_fouten = len(df_voorkeur) - df_voorkeur_hetzelfde['Huisadres'].nunique()
    return aantal_fouten
    
# Wens 4 - Aantal buren aan tafel. Prioriteit 5
def Wens4(df,buren):
    '''
    Wens4 eist als input df, een feasible solution en df_buren uit de dataset.
    Wens5 gaat kijken hoevaak in de df, de wens is overschreden.
    Returnt een parameter.
    '''
    # Voeg aan de dataframe buren een aantal kolommen toe. Dit zijn voor alle gangen de kolommen:
    # Het adres van bewoner 1, het adres van bewoner 2 en of deze twee overeenkomen.
    # Die laatste kolom bestaat uit 1 voor de buren die samen eten en een 0 anders. 
    buren['VoorBewoner1'] = buren['Bewoner1'].map(df.set_index('Bewoner')['Voor'])
    buren['VoorBewoner2'] = buren['Bewoner2'].map(df.set_index('Bewoner')['Voor'])
    buren['VoorSamen'] = (buren['VoorBewoner1'] == buren['VoorBewoner2'])
    
    buren['HoofdBewoner1'] = buren['Bewoner1'].map(df.set_index('Bewoner')['Hoofd'])
    buren['HoofdBewoner2'] = buren['Bewoner2'].map(df.set_index('Bewoner')['Hoofd'])
    buren['HoofdSamen'] = (buren['HoofdBewoner1'] == buren['HoofdBewoner2'])
    
    buren['NaBewoner1'] = buren['Bewoner1'].map(df.set_index('Bewoner')['Na'])
    buren['NaBewoner2'] = buren['Bewoner2'].map(df.set_index('Bewoner')['Na'])
    buren['NaSamen'] = (buren['NaBewoner1'] == buren['NaBewoner2'])
    
    # Als je dit voor elke gang heb gedaan tel je alles bij elkaar op en krijg je het aantal keer dat buren samen eten.
    aantal_fouten = buren['VoorSamen'].sum() + buren['HoofdSamen'].sum() + buren['NaSamen'].sum()
    return aantal_fouten

# Wens5 - Tafelgenoot vorig jaar. Prioriteit 4
def Wens5(df1, tafelgenoot):
    '''
    Wens5 eist als input df, een feasible solution en df_tafelgenoot uit de dataset.
    Wens5 gaat kijken hoevaak in de df, de wens is overschreden.
    Returnt een parameter.
    '''
    # Bepaal de tafelgenoten van dit jaar
    def vind_tafelgenoten(gang):
        groepen = df1.groupby(gang)['Bewoner'].apply(list)
        tafelgenoten = []
        for bewoners in groepen:
            tafelgenoten.extend([(bewoner, tafelgenoot) for bewoner in bewoners for tafelgenoot in bewoners if bewoner != tafelgenoot])
        return tafelgenoten

    tafelgenoten_lijst = sum([vind_tafelgenoten(gang) for gang in ['Voor', 'Hoofd', 'Na']], [])
    tafelgenoten_df = pd.DataFrame(tafelgenoten_lijst, columns=['Bewoner1', 'Bewoner2'])
    
    # Vergelijk de resultaten met tafelgenoot
    df_overlap = pd.merge(tafelgenoten_df, tafelgenoot, how='inner', left_on=['Bewoner1', 'Bewoner2'], right_on=['Bewoner1', 'Bewoner2'])
    aantal_fouten = len(df_overlap)
    return aantal_fouten

#------------------------------------------------------------------------------------
# Wensen bijelkaar
def Wens(df,kookte,adressen,buren,tafelgenoot):
    '''
    Wens functie sommeert alle wensen 1 tot en met 5 bij elkaar.
    De wensen worden vermenigvuldigd met een weging.

    Returnt een parameter.
    '''
    resultaat_wens1 = 50 * Wens1(df)
    resultaat_wens2 = 10 * Wens2(df,kookte)
    resultaat_wens3 = 5 * Wens3(df,adressen)
    resultaat_wens4 = 0.5 * Wens4(df,buren)
    resultaat_wens5 = 1 * Wens5(df,tafelgenoot)
    
    totaal = resultaat_wens1 + resultaat_wens2 + resultaat_wens3 + resultaat_wens4 + resultaat_wens5

    return totaal

#------------------------------------------------------------------------------------
# Constraint Check
def Constraints(df,dataset):
    '''
    Constraint functie gaat de oplossing controleren of die voldoet aan de gegeven constraints uit de dataset.

    Als de oplossing voldoet aan alle constraints, returnt de functie: None
    Als er iets niet wordt voldaan, dan returnt hij een print en bijbehorende constraint.
    '''
    
    # Inlezen van dataset en oplossing
    
    Bewoners = pd.read_excel(dataset, sheet_name = 'Bewoners')
    adressen = pd.read_excel(dataset, sheet_name = 'Adressen')
    Paar = pd.read_excel(dataset, sheet_name = 'Paar blijft bij elkaar', header = 1)
    buren = pd.read_excel(dataset, sheet_name = 'Buren', header = 1)
    Kookte = pd.read_excel(dataset, sheet_name = 'Kookte vorig jaar', header = 1)
    Tafelgenoot = pd.read_excel(dataset, sheet_name = 'Tafelgenoot vorig jaar', header = 1)    
    
    # Constraint 1
    
    # Er wordt gekeken of elke deelnemer in totaal op 3 verschillende adressen een gang eet.
    Deelnemer_ongelijk_aan_3 = {}
    for deelnemer in df['Bewoner']:
        gangen = df[df['Bewoner']==deelnemer][['Voor','Hoofd','Na']].values[0]
        aantal_gangen = len(set(gangen))
        if aantal_gangen !=3:
            Deelnemer_ongelijk_aan_3[deelnemer] = aantal_gangen
    if len(Deelnemer_ongelijk_aan_3) > 0:
        print('Er wordt niet voldaan aan Constraint 1')
        
    # Constraint 2
    
    # Er wordt gekeken of op elk adres maar één soort gang wordt bereid.
    set_adres = set(df['Huisadres'])
    for adres in set_adres:
        if ( len( set( df[ df['Huisadres']==adres ]['kookt'].values ) )) != 1:
            print('Er wordt niet voldaan aan Constraint 2')

    # Constraint 3
    
    # Er wordt gekeken of elke bewoner gedurende de gang die hij/zij bereidt aanwezig is op zijn/haar adres.
    Checklijst = []
    df_kokend = df.dropna(subset=['kookt'])
    for deelnemer in range(len(df_kokend)):
        gang = df_kokend.iloc[deelnemer]['kookt']
        adressen_deelnemer1 = df_kokend.iloc[deelnemer][gang]
        adressen_deelnemer2 = df_kokend.iloc[deelnemer]['Huisadres']
        if adressen_deelnemer1 != adressen_deelnemer2:
            Checklijst.append(df_kokend.iloc[deelnemer]['Bewoner'])
    if len(Checklijst) > 0:
        print('Er wordt niet voldaan aan Constraint 3') 
        
    # Constraint 4
    
    # Er wordt gekeken of op elk huisadres dat een gang kookt, er niet te veel of te weinig aanwezigen zijn.  
    kokend = df.dropna(subset=['kookt'])
    aantal_adressen = {}
    for index_bewoners, rij in kokend.iterrows():
        if rij['Huisadres'] not in aantal_adressen:
            aantal_adressen[rij['Huisadres']] = rij['aantal'] 
    for adres in aantal_adressen:
        minimum = adressen[ adressen['Huisadres']== adres ]['Min groepsgrootte'].values
        maximum = adressen[ adressen['Huisadres']== adres ]['Max groepsgrootte'].values
        if aantal_adressen[adres]>maximum or aantal_adressen[adres]<minimum:
            print('Er wordt niet voldaan aan Constraint 4')
    
    # Constraint 5

    # Er wordt gekeken of de paren ten alle tijden bij elkaar blijven. 
    for paar,(d1,d2) in Paar.iterrows():
        adressen_deelnemer1 = df[ df['Bewoner']==d1 ][ ['Voor','Hoofd','Na'] ].values.tolist()
        adressen_deelnemer2 = df[ df['Bewoner']==d2 ][ ['Voor','Hoofd','Na'] ].values.tolist()
        if adressen_deelnemer1 != adressen_deelnemer2:
            print('Er wordt niet voldaan aan Constraint 5')

#------------------------------------------------------------------------------------

def simulated_annealing(df, maximale_iteraties=1200, start_temperatuur=1200, alpha=0.999):
    '''
    Wens functie wordt hier gebruikt om de objective funtion te meten.
    Switch_addresses functie wordt hier gebruikt om de buuroplossing te vinden.

    Returnt twee waardes, een nieuwe df met verwisselde waarde en haar bijbehorende objective function waarde.
    '''
    # Maak een kopie van de huidige feasible solution en bereken daarmee de kosten
    huidige_oplossing = df.copy()
    huidige_kosten = Wens(huidige_oplossing,kookte,adressen,buren,tafelgenoot) 
    
    beste_oplossing = huidige_oplossing.copy()
    beste_kosten = huidige_kosten

    temperatuur = start_temperatuur
    
    # Maak 2 lege lijsten voor het plotje
    lijst_beste_kosten = []
    lijst_huidige_kosten = []
    aantal_iteraties = list(range(maximale_iteraties))
    
    # Hier beginnen de iteraties en worden de adressen omgedraaid en de nieuwe kosten berekend
    for iteraties in range(maximale_iteraties):
        nieuwe_oplossing = switch_addresses(huidige_oplossing, paar)
        nieuwe_kosten = Wens(nieuwe_oplossing,kookte,adressen,buren,tafelgenoot)
        
        verschil_kosten = nieuwe_kosten - huidige_kosten
        
        # De nieuwe oplossing wordt altijd geaccepteerd als hij beter is dan de huidige oplossing.
        # Zo niet is er een kans dat de verslechtering alsnog wordt toegelaten.
        if verschil_kosten < 0 or random.uniform(0, 1) < math.exp(-verschil_kosten / temperatuur):
            huidige_oplossing = nieuwe_oplossing
            huidige_kosten = nieuwe_kosten
            
            # Als het een beter oplossing is worden de huidige kosten ook de beste kosten 
            if huidige_kosten < beste_kosten:
                beste_oplossing = huidige_oplossing.copy()
                beste_kosten = huidige_kosten
        
        # Na een iteratie wordt telkens de temperatuur afgekoeld
        temperatuur *= alpha
          
        lijst_beste_kosten.append(beste_kosten)
        lijst_huidige_kosten.append(huidige_kosten)
        
        print(f'iteratie = {iteraties}, cost = {beste_kosten}')
        
    # Hier worden alle resultaten gevisualiseerd    
    plt.plot(aantal_iteraties,lijst_beste_kosten,label='Bestkost')
    plt.plot(aantal_iteraties,lijst_huidige_kosten,color='r',label='Buurkost')
    plt.xlabel('Iteraties')
    plt.ylabel('Objective function')
    plt.legend(loc='upper right')
    plt.title('Simulated Annealing')
    plt.grid(True)
    plt.show()
    
    return beste_oplossing, beste_kosten

# Proces vaker uitvoeren in een for loop
# Resultaten opslaan in excel
# resultaten = []
# kosten = []
# herhaling = 10
# for i in range(herhaling):
#     resultaat,kost = simulated_annealing(df1,maximale_iteraties=20000)
#     resultaten.append(resultaat)
#     kosten.append(kost)
#     bestandsnaam = f'Oplossing {i}.xlsx'
#     resultaat.to_excel(bestandsnaam, index=False)
# print(kosten)

# Of een keer hoge iteratie
res,kos = simulated_annealing(df1, maximale_iteraties=120000)
res.to_excel('Oplossing 1.xlsx',index=False)