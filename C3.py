import pandas as pd

#inlezen input
Dataset2 = 'Running Dinner eerste oplossing 2021.xlsx'
oplossing = pd.read_excel(Dataset2)

# LHS: informatie voor elk deelnemer, uit constraints
#| Bewoner | Adres | kookt |
#| d1      | a1    | voor  |


# RHS: informatie voor elk deelnemer, uit de planning
#|Bewoner[kookt] = Voor, Hoofd, Na
#|Bewoner[Voor ] = 

# a = oplossing.iloc[0]['kookt']
# lhs = oplossing.iloc[0][a]
# rhs = oplossing.iloc[0]['Huisadres']
# print(lhs,rhs)


#ik loop nu tegen aan NaN values
# eerst mensen filteren die niet hoef te koken

#nog een check met de constr dataset
Dataset = 'Running Dinner dataset 2021.xlsx'
Bewoners = pd.read_excel(Dataset, sheet_name = 'Bewoners')


niet_kokend = oplossing[oplossing['kookt'].isna()]
kokend = oplossing.dropna(subset=['kookt'])


niet_kokend_check = set(Bewoners[Bewoners['Kookt niet']==1]['Huisadres'])
oplos_niet_kokend_check = set(niet_kokend['Huisadres'])

if oplos_niet_kokend_check == niet_kokend_check:
    print('planning voldoet aan de data')
else:
    print('niet kokende personen komt niet overeen met de data')


con3 = []
for i in range(len(kokend)):
    a = kokend.iloc[i]['kookt']
    lhs = kokend.iloc[i][a]
    rhs = kokend.iloc[i]['Huisadres']
    if lhs!=rhs:
        con3.append(kokend.iloc[i]['Bewoner'])
        print('Deze bewoners koken op een andere adres terwijl zij thuis moeten koken')
if len(con3)==0:
    print('voldoet constr 3')

print(kokend.iloc[0]['Voor'])
print(kokend.iloc[0]['Huisadres'])
