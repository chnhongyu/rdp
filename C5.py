import pandas as pd

# Constraint 5 checkt voor paar blijft bij elkaar
# 1. uit de RDP dataset uithalen welke deelnemers dat zijn
# 2. (d1 , d2) er uit halen
# 3. d1, d2 uit de RDP oplossing bestand lezen
# 4.  'Voor Hoofd Na' kijken voor deze twee personen
# als het gelijk is dan voldoet het aan constraint 5
# 
# input: (RDP_oplossing, RDP_dataset)

oplossing = pd.read_excel('Running Dinner eerste oplossing 2021.xlsx')
dataset = pd.read_excel('Running Dinner dataset 2021.xlsx',sheet_name='Paar blijft bij elkaar',header=1)


def constraint5(RDP_oplossing, RDP_dataset):
    statement = True
    for paar,(d1,d2) in dataset.iterrows():
        lhs = oplossing[ oplossing['Bewoner']==d1 ][ ['Voor','Hoofd','Na'] ].values.tolist()
        rhs = oplossing[ oplossing['Bewoner']==d2 ][ ['Voor','Hoofd','Na'] ].values.tolist()
        if lhs != rhs:
            statement = False
    
    return print(statement)


constraint5(oplossing,dataset)