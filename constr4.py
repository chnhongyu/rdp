import pandas as pd

#inlezen input
Dataset1 = 'Running Dinner dataset 2021.xlsx'

Dataset2 = 'Running Dinner eerste oplossing 2021.xlsx'
oplossing = pd.read_excel(Dataset2)

Bewoners = pd.read_excel(Dataset1, sheet_name = 'Bewoners')

# daadwerkelijke aantal vergelijken met toegelaten aantal, voor elk adres

adres = set(oplossing['Huisadres'])
# print(adres)

con4 = []
for a in adres:
    con4.append(oplossing[oplossing['Huisadres']==a][['Huisadres','aantal']])
# print(con4)
# con4 returnt huisadres en aantal
print(oplossing[oplossing['Huisadres']=='V8'][['Huisadres','aantal']])