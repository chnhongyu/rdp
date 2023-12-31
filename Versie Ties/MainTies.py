import pandas as pd

def Constraints(Filepath_Dataset, Oplossing):
    
    ## Inlezen van dataset en oplossing
    
    Bewoners = pd.read_excel(Filepath_Dataset, sheet_name = 'Bewoners')
    Adressen = pd.read_excel(Filepath_Dataset, sheet_name = 'Adressen')
    Paar = pd.read_excel(Filepath_Dataset, sheet_name = 'Paar blijft bij elkaar', header = 1)
    Buren = pd.read_excel(Filepath_Dataset, sheet_name = 'Buren', header = 1)
    Kookte = pd.read_excel(Filepath_Dataset, sheet_name = 'Kookte vorig jaar', header = 1)
    Tafelgenoot = pd.read_excel(Filepath_Dataset, sheet_name = 'Tafelgenoot vorig jaar', header = 1)    
    
    Constraint = []
    
    ## Constraint 1
    
    Deelnemer_ongelijk_aan_3 = {}
    for deelnemer in Oplossing['Bewoner']:
        gangen = Oplossing[Oplossing['Bewoner']==deelnemer][['Voor','Hoofd','Na']].values[0]
        aantal_gangen = len(set(gangen))
        if aantal_gangen !=3:
            Deelnemer_ongelijk_aan_3[deelnemer] = aantal_gangen
    if len(Deelnemer_ongelijk_aan_3) > 0:
        Constraint.append('Er wordt niet voldaan aan Constraint 1')
        
    ## Constraint 2
    
    set_adres = set(Oplossing['Huisadres'])
    for adres in set_adres:
        if ( len( set( Oplossing[ Oplossing['Huisadres']==adres ]['kookt'].values ) )) != 1:
            Constraint.append('Er wordt niet voldaan aan Constraint 2')

    ## Constraint 3
    
    Checklijst = []
    df_kokend = Oplossing.dropna(subset=['kookt'])
    for deelnemer in range(len(df_kokend)):
        gang = df_kokend.iloc[deelnemer]['kookt']
        lhs = df_kokend.iloc[deelnemer][gang]
        rhs = df_kokend.iloc[deelnemer]['Huisadres']
        if lhs != rhs:
            Checklijst.append(df_kokend.iloc[deelnemer]['Bewoner'])
    if len(Checklijst) > 0:
        Constraint.append('Er wordt niet voldaan aan Constraint 3')
        
    ## Constraint 4
    
    kokend = Oplossing.dropna(subset=['kookt'])
    adres_count = {}
    for index_bewoners, rij in kokend.iterrows():
        if rij['Huisadres'] not in adres_count:
            adres_count[rij['Huisadres']] = rij['aantal'] 
    for a in adres_count:
        lb = Adressen[ Adressen['Huisadres']== a ]['Min groepsgrootte'].values
        ub = Adressen[ Adressen['Huisadres']== a ]['Max groepsgrootte'].values
        if adres_count[a]>ub or adres_count[a]<lb:
            Constraint.append('Er wordt niet voldaan aan Constraint 4')
    
    ## Constraint 5

    for paar,(d1,d2) in Paar.iterrows():
        lhs = Oplossing[ Oplossing['Bewoner']==d1 ][ ['Voor','Hoofd','Na'] ].values.tolist()
        rhs = Oplossing[ Oplossing['Bewoner']==d2 ][ ['Voor','Hoofd','Na'] ].values.tolist()
        if lhs != rhs:
            Constraint.append('Er wordt niet voldaan aan Constraint 5')
    
    if len(Constraint) == 0:
        Constraint.append('Toegelaten')
    
    return Constraint

def Wensen(Oplossing, Kookte, Adressen, Buren, Tafelgenoot):
    
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
    
    Niveau = 2*Wens1 + 10*Wens2 + 10*Wens3 + 3*Wens4 + 1*Wens5
    
    return Niveau 
