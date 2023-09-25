import pandas as pd

#inlezen input
Dataset1 = 'Running Dinner dataset 2021.xlsx'
Bewoners = pd.read_excel(Dataset1, sheet_name = 'Bewoners')
Dataset2 = 'Running Dinner eerste oplossing 2021.xlsx'
oplossing = pd.read_excel(Dataset2)

Adressen = pd.read_excel(Dataset1, sheet_name = 'Adressen')
lb = Adressen[['Huisadres','Min groepsgrootte']].dropna()
ub = Adressen[['Huisadres','Max groepsgrootte']].dropna()

# daadwerkelijke aantal vergelijken met toegelaten aantal, voor elk adres


# verdelen in twee soorten adressen, adressen die moet koken en adressen die niet hoeft te koken
#niet kokende adressen uit oplossing
niet_kokend = oplossing[oplossing['kookt'].isna()]
kokend = oplossing.dropna(subset=['kookt'])

# niet kokende adressen uit dataset
niet_kokend_check = set(Bewoners[Bewoners['Kookt niet']==1]['Huisadres'])
oplos_niet_kokend_check = set(niet_kokend['Huisadres'])


adres = set(oplossing['Huisadres'])
# set van adressen


# maak een df voor elk adres en aantal count.
voor = oplossing['Voor'].value_counts()
hoofd = oplossing['Hoofd'].value_counts()
na = oplossing['Na'].value_counts()
count_voor_elk_a = pd.concat([voor,hoofd,na])
# print(count_voor_elk_a)
cvea = pd.DataFrame(count_voor_elk_a)
cvea = cvea.rename(columns={'index': 'Adres'}).reset_index(drop=True)
print(cvea)


# goede_adressen = []
# foute_adressen = []
# for a in adres:
#     if  lb[lb['Huisadres']==a]['Min groepsgrootte']<= count_voor_elk_a[count_voor_elk_a['Huisadres']==a] <= ub[ ub['Huisadres']==a ]['Max groepsgrootte']:
#         goede_adressen.append(a)
#     else:
#         foute_adressen.append(a)






# con4 = []
# for a in adres:
#     if (lb[lb['Huisadres']==a]['Min groepsgrootte']) <= (oplossing[oplossing['Huisadres']==a]['aantal'].unique()) <= (ub[ub['Huisadres']==a]['Max groepsgrootte']) :
#         con4.append(oplossing[oplossing['Huisadres']==a][['Huisadres','aantal']])
# print(con4)
# # con4 returnt huisadres en aantal

# print(lb[lb['Huisadres']=='V12']['Min groepsgrootte'])
# print(oplossing[oplossing['Huisadres']=='V12']['aantal'].unique())
# print(ub[ub['Huisadres']=='V12']['Max groepsgrootte'])