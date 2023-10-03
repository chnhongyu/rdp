import pandas as pd

def Constraints(Filepath_Dataset, Oplossing):
    
    ## Inlezen van dataset en oplossing
    
    Bewoners = pd.read_excel(Filepath_Dataset, sheet_name = 'Bewoners')
    Adressen = pd.read_excel(Filepath_Dataset, sheet_name = 'Adressen')
    Paar = pd.read_excel(Filepath_Dataset, sheet_name = 'Paar blijft bij elkaar', header = 1)
    Buren = pd.read_excel(Filepath_Dataset, sheet_name = 'Buren', header = 1)
    Kookte = pd.read_excel(Filepath_Dataset, sheet_name = 'Kookte vorig jaar', header = 1)
    Tafelgenoot = pd.read_excel(Filepath_Dataset, sheet_name = 'Tafelgenoot vorig jaar', header = 1)    
    
    ## Constraint 1
    
    Deelnemer_ongelijk_aan_3 = {}
    for deelnemer in Oplossing['Bewoner']:
        gangen = Oplossing[Oplossing['Bewoner']==deelnemer][['Voor','Hoofd','Na']].values[0]
        aantal_gangen = len(set(gangen))
        if aantal_gangen !=3:
            Deelnemer_ongelijk_aan_3[deelnemer] = aantal_gangen
    if len(Deelnemer_ongelijk_aan_3) > 0:
        print('Er wordt niet voldaan aan Constraint 1')
        
    ## Constraint 2
    
    set_adres = set(Oplossing['Huisadres'])
    for adres in set_adres:
        if ( len( set( Oplossing[ Oplossing['Huisadres']==adres ]['kookt'].values ) )) != 1:
            print('Er wordt niet voldaan aan Constraint 2')

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
        print('Er wordt niet voldaan aan Constraint 3') 
        
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
            print('Er wordt niet voldaan aan Constraint 4')
    
    ## Constraint 5

    for paar,(d1,d2) in Paar.iterrows():
        lhs = Oplossing[ Oplossing['Bewoner']==d1 ][ ['Voor','Hoofd','Na'] ].values.tolist()
        rhs = Oplossing[ Oplossing['Bewoner']==d2 ][ ['Voor','Hoofd','Na'] ].values.tolist()
        if lhs != rhs:
            print('Er wordt niet voldaan aan Constraint 5')

def Wensen(Oplossing, Kookte, Adressen, Buren, Tafelgenoot):
    
    ## Wens 1
        
    Wens1 = 0
    bewoner_data = {}
    for index, row in Oplossing.iterrows():
        bewoner = row['Bewoner']
        voor = row['Voor']
        hoofd = row['Hoofd']
        na = row['Na']
        bewoner_data[bewoner] = [voor, hoofd, na]
    for bewoner1, waarden1 in bewoner_data.items():
        for bewoner2, waarden2 in bewoner_data.items():
            if bewoner1 != bewoner2:  
                overeenkomende_waarden = set(waarden1) & set(waarden2)
                if len(overeenkomende_waarden) == 2:
                    Wens1 += 1
                if len(overeenkomende_waarden) == 3:
                    Wens1 += 2
            
    ## Wens 2
    
    df_koken_hetzelfde = Oplossing.merge(Kookte, left_on=['Huisadres', 'kookt'], right_on=['Huisadres', 'Gang'], how='inner')
    Wens2 = df_koken_hetzelfde['Huisadres'].nunique()
    
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
    
    Tafelgenoot['Huisadres1'] = Tafelgenoot['Bewoner1'].map(Oplossing.set_index('Bewoner')['Huisadres'])
    Tafelgenoot['Huisadres2'] = Tafelgenoot['Bewoner2'].map(Oplossing.set_index('Bewoner')['Huisadres'])
    Tafelgenoot['VoorBewoner1'] = Tafelgenoot['Bewoner1'].map(Oplossing.set_index('Bewoner')['Voor'])
    Tafelgenoot['VoorBewoner2'] = Tafelgenoot['Bewoner2'].map(Oplossing.set_index('Bewoner')['Voor'])
    Tafelgenoot['VoorSamen'] = (Tafelgenoot['Huisadres1'] != Tafelgenoot['Huisadres2']) & (Tafelgenoot['VoorBewoner1'] == Tafelgenoot['VoorBewoner2'])
    Tafelgenoot['HoofdBewoner1'] = Tafelgenoot['Bewoner1'].map(Oplossing.set_index('Bewoner')['Hoofd'])
    Tafelgenoot['HoofdBewoner2'] = Tafelgenoot['Bewoner2'].map(Oplossing.set_index('Bewoner')['Hoofd'])
    Tafelgenoot['HoofdSamen'] = (Tafelgenoot['Huisadres1'] != Tafelgenoot['Huisadres2']) & (Tafelgenoot['HoofdBewoner1'] == Tafelgenoot['HoofdBewoner2'])
    Tafelgenoot['NaBewoner1'] = Tafelgenoot['Bewoner1'].map(Oplossing.set_index('Bewoner')['Na'])
    Tafelgenoot['NaBewoner2'] = Tafelgenoot['Bewoner2'].map(Oplossing.set_index('Bewoner')['Na'])
    Tafelgenoot['NaSamen'] = (Tafelgenoot['Huisadres1'] != Tafelgenoot['Huisadres2']) & (Tafelgenoot['HoofdBewoner1'] == Tafelgenoot['HoofdBewoner2'])
    Wens5 = Tafelgenoot['VoorSamen'].sum() + Tafelgenoot['HoofdSamen'].sum() + Tafelgenoot['NaSamen'].sum()

    ## Kwaliteit oplossing
    
    Niveau = Wens1 + Wens2 + Wens3 + Wens4 + Wens5
    
    return Niveau 
    
    
