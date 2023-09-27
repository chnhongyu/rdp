import pandas as pd

def Constraint(Filepath_Dataset, Filepath_Oplossing):
    
    ## Inlezen van dataset en oplossing
    
    Oplossing = pd.read_excel(Filepath_Oplossing)
    
    Bewoners = pd.read_excel(Filepath_Dataset, sheet_name = 'Bewoners')
    Adressen = pd.read_excel(Filepath_Dataset, sheet_name = 'Adressen')
    Paar = pd.read_excel(Filepath_Dataset, sheet_name = 'Paar blijft bij elkaar', header = 1)
    Buren = pd.read_excel(Filepath_Dataset, sheet_name = 'Buren', header = 1)
    Kookte = pd.read_excel(Filepath_Dataset, sheet_name = 'Kookte vorig jaar', header = 1)
    Tafelgenoot = pd.read_excel(Filepath_Dataset, sheet_name = 'Tafelgenoot vorig jaar', header = 1)
    
    Statement = True
    
    ## Constraint 1
    
    Deelnemer_ongelijk_aan_3 = {}
    for deelnemer in Oplossing['Bewoner']:
        gangen = Oplossing[Oplossing['Bewoner']==deelnemer][['Voor','Hoofd','Na']].values[0]
        aantal_gangen = len(set(gangen))
        if aantal_gangen !=3:
            Deelnemer_ongelijk_aan_3[deelnemer] = aantal_gangen
    if len(Deelnemer_ongelijk_aan_3) >0:
        statement = False
        
    ## Constraint 2
    
    

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
        statement = False    
        
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
            statement= False
    
    ## Constraint 5

    for paar,(d1,d2) in dataset.iterrows():
        lhs = Paar[ Paar['Bewoner']==d1 ][ ['Voor','Hoofd','Na'] ].values.tolist()
        rhs = Paar[ Paar['Bewoner']==d2 ][ ['Voor','Hoofd','Na'] ].values.tolist()
        if lhs != rhs:
            statement = False
    

    
    
    