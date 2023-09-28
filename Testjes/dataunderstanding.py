import pandas as pd

#inlezen input
Data = 'Running Dinner eerste oplossing 2021.xlsx'
df = pd.read_excel(Data)

kook_dict = {"Voor": [], "Hoofd": [], "Na": []}

for index, row in df.iterrows():
    huisadres = row["Huisadres"]
    kookt = row["kookt"]
    
    # Voeg het huisadres toe aan de juiste kookvoorkeur
    if kookt in kook_dict:
        kook_dict[kookt].append(huisadres)

voor = kook_dict['Voor']
hoofd = kook_dict['Hoofd']
na = kook_dict['Na']
print(voor)
print(hoofd)
print(na)
#print(len(voor),len(hoofd),len(na))