import pandas as pd
import numpy as np
import random
import math

#Inlezen dataset en feasible solution
dataset = 'Running Dinner dataset 2023 v2.xlsx'
oplossing1 = 'Running Dinner eerste oplossing 2023 v2.xlsx'

#DFs van dataset
bewoners = pd.read_excel(dataset,sheet_name='Bewoners')
adressen = pd.read_excel(dataset,sheet_name='Adressen')
paar = pd.read_excel(dataset,sheet_name='Paar blijft bij elkaar',header = 1)
buren = pd.read_excel(dataset,sheet_name='Buren',header = 1)
kookte = pd.read_excel(dataset,sheet_name='Kookte vorig jaar',header = 1)
tafelgenoot = pd.read_excel(dataset,sheet_name='Tafelgenoot vorig jaar',header = 1)
#Feasible solution
oplossing = pd.read_excel(oplossing1)

#df staat voor df_oplossing!
df = oplossing

random_gang = 'Voor'

bewoner1_index = 120
bewoner1 = df.loc[bewoner1_index, "Bewoner"]
adres1 = df.loc[bewoner1_index, random_gang]

print(f"Geselecteerde bewoner1 (niet kokend): {bewoner1} met adres: {adres1}. index = {bewoner1_index}")

bewoner2 = None
if bewoner1 in paar['Bewoner1'].values:
    bewoner2 = paar[paar['Bewoner1'] == bewoner1]['Bewoner2'].values[0]
elif bewoner1 in paar['Bewoner2'].values:
    bewoner2 = paar[paar['Bewoner2'] == bewoner1]['Bewoner1'].values[0]
    
if bewoner2:
    bewoner2_index = df[df["Bewoner"] == bewoner2].index[0]
    adres2 = df.loc[bewoner2_index, random_gang]
    print(f"Bewoner1 {bewoner1} heeft een paar: {bewoner2} met adres: {adres2}. index={bewoner2_index}")

if bewoner2:
    bewoner2_index = df[df["Bewoner"] == bewoner2].index[0]
    print(f"Bewoner1 {bewoner1} heeft een paar: {bewoner2}")

    # Selecteer een ander paar om adressen mee te ruilen
    andere_paren_indices = paar[
        (~paar['Bewoner1'].isin([bewoner1, bewoner2])) & 
        (~paar['Bewoner2'].isin([bewoner1, bewoner2]))].index.tolist()
    random_paar_index = random.choice(andere_paren_indices)
    bewoner3 = paar.loc[random_paar_index, "Bewoner1"]
    bewoner4 = paar.loc[random_paar_index, "Bewoner2"]

    bewoner3_index = df[df["Bewoner"] == bewoner3].index[0]
    bewoner4_index = df[df["Bewoner"] == bewoner4].index[0]

        # Adressen wisselen
    df.loc[bewoner1_index, random_gang], df.loc[bewoner2_index, random_gang], df.loc[bewoner3_index, random_gang], df.loc[bewoner4_index, random_gang] = \
        df.loc[bewoner3_index, random_gang], df.loc[bewoner4_index, random_gang], df.loc[bewoner1_index, random_gang], df.loc[bewoner2_index, random_gang]

    print(f"Adressen van {bewoner1} en {bewoner2} zijn verwisseld met {bewoner3} en {bewoner4}")