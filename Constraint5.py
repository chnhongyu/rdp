def Constraint5(Paar, Oplossing):
    Status = True
    for index, row in Paar.iterrows():
        Bewoner1 = row['Bewoner1']
        Bewoner2 = row['Bewoner2']
        for index, row in Oplossing.iterrows():
            if row['Bewoner'] == Bewoner1:
                Adressen1 = [row['Voor'], row['Hoofd'], row['Na']]
            if row['Bewoner'] == Bewoner2:
                Adressen2 = [row['Voor'], row['Hoofd'], row['Na']]
        if Adressen1 != Adressen2:
            Status = False
    return Status
    

            
