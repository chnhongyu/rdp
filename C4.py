import pandas as pd

oplossing = pd.read_excel('Running Dinner eerste oplossing 2021.xlsx')
dataset = pd.read_excel('Running Dinner dataset 2021.xlsx',sheet_name='Adressen')


# voor elk adres, aantal = count
# constr 4 checkt of aantal voor elk adres binnen de interval valt


# drop ook alle adressen waar niet gekookt hoef te worden
kokend = oplossing.dropna(subset=['kookt'])

# print(kokend)

adres_gang = {}
adres_count = {}
for index_bewoners, rij in kokend.iterrows():
    if rij['Huisadres'] not in adres_gang:
        adres_gang[rij['Huisadres']] = rij['kookt']
    if rij['Huisadres'] not in adres_count:
        adres_count[rij['Huisadres']] = rij['aantal']

# adres_gang en adres_count zijn twee dictionaries.
# print(adres_gang)
# print(adres_count)

# df = pd.DataFrame(list(adres_count.items()), columns=['adres', 'aantal'])
# print(df)

#----------------------------------------------
# nu dataset bewerken
statement = True
for adres in adres_count:
    lb = dataset[ dataset['Huisadres']== adres ]['Min groepsgrootte'].values
    ub = dataset[ dataset['Huisadres']== adres ]['Max groepsgrootte'].values
    if adres_count[a]>ub or adres_count[a]<lb:
        statement= False
print(statement)

