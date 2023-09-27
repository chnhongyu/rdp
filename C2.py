import pandas as pd

oplossing = oplossing = pd.read_excel('Running Dinner eerste oplossing 2021.xlsx')

#constraint 2 kijkt voor elk adres, wat onder kookt staat gelijk moet zijn aan elkaar

set_adres = set(oplossing['Huisadres'])
print(set_adres)