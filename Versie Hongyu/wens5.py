import pandas as pd
import numpy as np

dataset = 'Running Dinner dataset 2023 v2.xlsx'
oplossing1 = 'Running Dinner tweede oplossing 2023 v2.xlsx'


bewoners = pd.read_excel(dataset,sheet_name='Bewoners')
adressen = pd.read_excel(dataset,sheet_name='Adressen')
paar = pd.read_excel(dataset,sheet_name='Paar blijft bij elkaar',header = 1)
buren = pd.read_excel(dataset,sheet_name='Buren',header = 1)
kookte = pd.read_excel(dataset,sheet_name='Kookte vorig jaar',header = 1)
tafelgenoot = pd.read_excel(dataset,sheet_name='Tafelgenoot vorig jaar',header = 1)

oplossing = pd.read_excel(oplossing1)

df1 = oplossing
def count_matching_tafelgenoten(df1, tafelgenoot):
    # Stap 1: Bepaal de tafelgenoten van dit jaar
    def find_tafelgenoten(gang):
        groepen = df1.groupby(gang)['Bewoner'].apply(list)
        tafelgenoten = []
        for bewoners in groepen:
            tafelgenoten.extend([(bewoner, genoot) for bewoner in bewoners for genoot in bewoners if bewoner != genoot])
        return tafelgenoten

    tafelgenoten_list = sum([find_tafelgenoten(gang) for gang in ['Voor', 'Hoofd', 'Na']], [])
    tafelgenoten_df = pd.DataFrame(tafelgenoten_list, columns=['Bewoner1', 'Bewoner2'])
    print(tafelgenoten_df)
    
    # Stap 2: Vergelijk de resultaten met tafelgenoot
    merged_df = pd.merge(tafelgenoten_df, tafelgenoot, how='inner', left_on=['Bewoner1', 'Bewoner2'], right_on=['Bewoner1', 'Bewoner2'])
    print(merged_df)
    return len(merged_df)

# Voorbeeld van hoe de functie aan te roepen
count = count_matching_tafelgenoten(df1, tafelgenoot)
print(count)
