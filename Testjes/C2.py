import pandas as pd

oplossing = oplossing = pd.read_excel('Running Dinner eerste oplossing 2021.xlsx')

#constraint 2 kijkt voor elk adres, wat onder kookt staat gelijk moet zijn aan elkaar

set_adres = set(oplossing['Huisadres'])

print(len(set(oplossing[oplossing['Huisadres']=='V12' ]['kookt'].values)))


check = []
statement = True

for adres in set_adres:
    if ( len( set( oplossing[ oplossing['Huisadres']==adres ]['kookt'].values ) )) != 1:
        check.append(adres)
        statement = False
print(statement)