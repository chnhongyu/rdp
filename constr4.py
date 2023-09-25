import pandas as pd

#inlezen input
Dataset1 = 'Running Dinner dataset 2021.xlsx'

Dataset2 = 'Running Dinner eerste oplossing 2021.xlsx'
oplossing = pd.read_excel(Dataset2)

Adressen = pd.read_excel(Dataset1, sheet_name = 'Adressen')
lb = Adressen[['Huisadres','Min groepsgrootte']]
ub = Adressen[['Huisadres','Max groepsgrootte']]
print(lb)
# daadwerkelijke aantal vergelijken met toegelaten aantal, voor elk adres


# verdelen in twee soorten adressen, adressen die moet koken en adressen die niet hoeft te koken
niet_kokend = oplossing[oplossing['kookt'].isna()]
kokend = oplossing.dropna(subset=['kookt'])


adres = set(oplossing['Huisadres'])
# set van adressen



# con4 = []
# for a in adres:
#     # if (lb[lb['Huisadres']==a]) <= (oplossing[oplossing['Huisadres']==a]['aantal']) <= (ub[ub['Huisadres']==a]) :
#         con4.append(oplossing[oplossing['Huisadres']==a][['Huisadres','aantal']])
# print(con4)
# # con4 returnt huisadres en aantal
# print()

