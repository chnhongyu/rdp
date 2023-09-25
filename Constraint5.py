import pandas as pd

Dataset2 = 'Running Dinner eerste oplossing 2021.xlsx'
oplossing = pd.read_excel(Dataset2)

Dataset = 'Running Dinner dataset 2021.xlsx'
Bewoners = pd.read_excel(Dataset, sheet_name = 'Bewoners')
Adressen = pd.read_excel(Dataset, sheet_name = 'Adressen')
Paar = pd.read_excel(Dataset, sheet_name = 'Paar blijft bij elkaar', header = 1)
Buren = pd.read_excel(Dataset, sheet_name = 'Buren', header = 1)
Kookte = pd.read_excel(Dataset, sheet_name = 'Kookte vorig jaar', header = 1)
Tafelgenoot = pd.read_excel(Dataset, sheet_name = 'Tafelgenoot vorig jaar', header = 1)

Dataset3 = 'Running Dinner eerste oplossing 2022.xlsx'
oplossing2 = pd.read_excel(Dataset3)

Dataset4 = 'Running Dinner dataset 2022.xlsx'
Bewoners2 = pd.read_excel(Dataset4, sheet_name = 'Bewoners')
Adressen2 = pd.read_excel(Dataset4, sheet_name = 'Adressen')
Paar2 = pd.read_excel(Dataset4, sheet_name = 'Paar blijft bij elkaar', header = 1)
Buren2 = pd.read_excel(Dataset4, sheet_name = 'Buren', header = 1)
Kookte2 = pd.read_excel(Dataset4, sheet_name = 'Kookte vorig jaar', header = 1)
Tafelgenoot2 = pd.read_excel(Dataset4, sheet_name = 'Tafelgenoot vorig jaar', header = 1)

for index, row in Paar.iterrows():
    Bewoner1 = row['Bewoner1']
    Bewoner2 = row['Bewoner2']
    for index, row in oplossing.iterrows():
        if row['Bewoner'] == Bewoner1:
            Adressen1 = [row['Voor'], row['Hoofd'], row['Na']]
        if row['Bewoner'] == Bewoner2:
            Adressen2 = [row['Voor'], row['Hoofd'], row['Na']]
    if Adressen1 != Adressen2:
        print(f'paar {Bewoner1} en {Bewoner2} zitten niet elke gang bij elkaar')
    

            
