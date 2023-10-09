# Importeren libraries 
import pandas as pd
import random
import math
import matplotlib.pyplot as plt

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
df = oplossing

def paar_naar_tuple(df,paar):
    paren = []
    for _,rij in paar.iterrows():
        index_deelnemer1 = df[df['Bewoner'] == rij['Bewoner1']].index[0]
        index_deelnemer2 = df[df['Bewoner'] == rij['Bewoner2']].index[0]
        paren.append((index_deelnemer1,index_deelnemer2))
    return  paren

paren = paar_naar_tuple(df,paar)
print(paren)


for i in paren:
    print(i[0],i[1])